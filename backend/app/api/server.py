import asyncio
import queue
import threading
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from app.pipeline.creator_pipeline import run_pipeline
from app.api.logger import log_capture
from app.database.supabase import supabase
from app.outreach.email import send_email
from app.utils.cancellation import reset_stop, request_stop, PipelineStoppedException
from pydantic import BaseModel, Field
from typing import List, Optional


class RunConfig(BaseModel):
    keywords: Optional[str] = None
    target_profiles: Optional[int] = Field(default=None, ge=1, le=50)


app = FastAPI(title="Creator Scraper API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline_running = False
pipeline_lock = threading.Lock()


def run_scraper_bg(keywords=None, target_profiles=None):
    global pipeline_running
    try:
        run_pipeline(keywords=keywords, target_profiles=target_profiles)
    except PipelineStoppedException:
        print("\nPipeline was stopped by user request.")
    except Exception as e:
        print(f"\nPipeline failed with error: {e}")
    finally:
        with pipeline_lock:
            pipeline_running = False
        # Stop log redirection
        log_capture.stop()
        print("\nPipeline run complete.")


@app.post("/api/run")
def start_pipeline(config: Optional[RunConfig] = None):
    global pipeline_running
    with pipeline_lock:
        if pipeline_running:
            raise HTTPException(status_code=400, detail="Pipeline is already running")
        pipeline_running = True

    keywords_list = None
    target_profiles = None
    if config:
        if config.keywords:
            keywords_list = [k.strip() for k in config.keywords.split(",") if k.strip()]
        if config.target_profiles is not None:
            # Additional safety check
            if config.target_profiles > 50:
                raise HTTPException(
                    status_code=400, detail="Search people count cannot be more than 50"
                )
            target_profiles = config.target_profiles

    reset_stop()

    log_capture.start()

    thread = threading.Thread(
        target=run_scraper_bg, args=(keywords_list, target_profiles), daemon=True
    )
    thread.start()

    return {"status": "started", "message": "Pipeline execution started in background."}


@app.get("/api/status")
def get_pipeline_status():
    global pipeline_running
    return {"running": pipeline_running}


@app.post("/api/stop")
def stop_pipeline():
    global pipeline_running
    with pipeline_lock:
        if not pipeline_running:
            raise HTTPException(status_code=400, detail="Pipeline is not running")
        request_stop()
    return {"status": "stopping", "message": "Pipeline stop requested."}


@app.get("/api/stream")
async def stream_logs():
    """
    Server-Sent Events endpoint to stream stdout logs.
    """
    log_queue = queue.Queue(maxsize=2000)
    log_capture.register(log_queue)

    async def event_generator():
        try:
            while True:
                while not log_queue.empty():
                    message = log_queue.get_nowait()
                    yield {"data": message}
                await asyncio.sleep(0.05)
        except asyncio.CancelledError:
            pass
        finally:
            log_capture.unregister(log_queue)

    return EventSourceResponse(event_generator())


@app.get("/api/db/creators")
def get_creators_table():
    try:
        response = supabase.table("creators").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database fetch failed: {str(e)}")


@app.get("/api/db/reels")
def get_reels_table():
    try:
        response = supabase.table("reels").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database fetch failed: {str(e)}")


@app.get("/api/db/outreach")
def get_outreach_table():
    try:
        response = supabase.table("outreach").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database fetch failed: {str(e)}")


@app.post("/api/outreach/send/{creator_id}")
def send_outreach_email(creator_id: int):
    """
    Trigger sending the generated email outreach to a specific creator.
    """
    try:
        outreach_res = (
            supabase.table("outreach")
            .select("*")
            .eq("creator_id", creator_id)
            .execute()
        )
        if not outreach_res.data:
            raise HTTPException(
                status_code=404, detail="No outreach draft found for this creator ID"
            )
        draft = outreach_res.data[0]

        creator_res = (
            supabase.table("creators")
            .select("contact_email, username")
            .eq("id", creator_id)
            .execute()
        )
        if not creator_res.data:
            raise HTTPException(status_code=404, detail="Creator details not found")
        creator = creator_res.data[0]

        to_email = creator.get("contact_email")
        if not to_email or to_email == "Not Found":
            raise HTTPException(
                status_code=400,
                detail=f"No valid contact email found for @{creator.get('username')}",
            )

        supabase.table("outreach").update({"email_status": "sending"}).eq(
            "creator_id", creator_id
        ).execute()

        send_email(
            to_email=to_email,
            subject=draft.get("email_subject"),
            body=draft.get("email_body"),
        )

        supabase.table("outreach").update({"email_status": "sent"}).eq(
            "creator_id", creator_id
        ).execute()

        return {
            "status": "success",
            "message": f"Email successfully sent to {to_email}",
        }

    except Exception as e:
        try:
            supabase.table("outreach").update({"email_status": "failed"}).eq(
                "creator_id", creator_id
            ).execute()
        except:
            pass
        raise HTTPException(status_code=500, detail=str(e))
