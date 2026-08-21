import sys
import uvicorn
from app.pipeline.creator_pipeline import run_pipeline

if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_pipeline()
    else:
        print("Starting Creator Scraper API server on http://localhost:8000...")
        uvicorn.run("app.api.server:app", host="127.0.0.1", port=8000, reload=True)
