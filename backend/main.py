import sys
import uvicorn
from app.pipeline.creator_pipeline import run_pipeline
import os

if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_pipeline()
    else:
        print("Starting Creator Scraper API server on http://localhost:8000...")
        port = int(os.environ.get("PORT", 8000))
        uvicorn.run(app, host="0.0.0.0", port=port)
