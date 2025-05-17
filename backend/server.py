from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn
import sys
import asyncio
from typing import Dict, Any, List
from pydantic import BaseModel

# Add the current directory to the path so we can import the bot module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our Instagram bot
from bot.instagram_bot import InstagramBot

app = FastAPI(title="Instagram Engagement Bot API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize bot
instagram_bot = InstagramBot()

# Models for API requests/responses
class StatusResponse(BaseModel):
    status: str
    message: str

class StatsResponse(BaseModel):
    user_stats: Dict[str, Any]
    engagement_stats: List[Dict[str, Any]]
    hashtags: List[str]
    configuration: Dict[str, Any]

# Background task for running scraping job
async def run_scraping_job_task():
    await instagram_bot.run_scraping_job()

@app.get("/api/status")
async def get_status():
    """Get the current status of the bot."""
    return {"status": "online", "message": "Instagram engagement bot is running"}

@app.post("/api/scraping/start")
async def start_scraping(background_tasks: BackgroundTasks):
    """Start a scraping job in the background."""
    background_tasks.add_task(run_scraping_job_task)
    return {"status": "success", "message": "Scraping job started in background"}

@app.post("/api/scheduler/start")
async def start_scheduler():
    """Start the engagement scheduler."""
    instagram_bot.start_scheduler()
    return {"status": "success", "message": "Engagement scheduler started"}

@app.post("/api/scheduler/stop")
async def stop_scheduler():
    """Stop the engagement scheduler."""
    instagram_bot.stop_scheduler()
    return {"status": "success", "message": "Engagement scheduler stopped"}

@app.get("/api/stats")
async def get_stats():
    """Get bot statistics."""
    stats = await instagram_bot.get_stats()
    return stats

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8001, reload=True)
