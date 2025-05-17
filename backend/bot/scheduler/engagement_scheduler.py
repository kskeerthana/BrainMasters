import os
import logging
import schedule
import time
import random
import threading
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Import our modules
from ..models.schemas import EngagementRecord
from ..automation.instagram_automator import InstagramAutomator
from ..db.supabase_client import SupabaseClient

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent.parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EngagementScheduler:
    def __init__(self):
        self.supabase = SupabaseClient()
        self.automator = None
        self.running = False
        self.thread = None
        
        # Load configuration from environment variables
        self.max_engagements_per_day = int(os.environ.get("MAX_USERS_PER_DAY", 10))
        
        # Track daily engagement count
        self.daily_engagement_count = 0
        self.last_reset_date = datetime.now().date()
    
    def start(self):
        """Start the engagement scheduler."""
        if self.running:
            logger.warning("Scheduler is already running")
            return
        
        logger.info("Starting engagement scheduler")
        self.running = True
        
        # Reset counters
        self.daily_engagement_count = 0
        self.last_reset_date = datetime.now().date()
        
        # Define schedule
        # Run engagement jobs at random times throughout the day to mimic human behavior
        
        # Morning engagement (8-10 AM)
        morning_hour = random.randint(8, 10)
        morning_minute = random.randint(0, 59)
        schedule.every().day.at(f"{morning_hour:02d}:{morning_minute:02d}").do(self.process_pending_engagements)
        
        # Midday engagement (12-2 PM)
        midday_hour = random.randint(12, 14)
        midday_minute = random.randint(0, 59)
        schedule.every().day.at(f"{midday_hour:02d}:{midday_minute:02d}").do(self.process_pending_engagements)
        
        # Evening engagement (6-8 PM)
        evening_hour = random.randint(18, 20)
        evening_minute = random.randint(0, 59)
        schedule.every().day.at(f"{evening_hour:02d}:{evening_minute:02d}").do(self.process_pending_engagements)
        
        # Also run every few hours for any urgent engagements
        schedule.every(3).hours.do(self.process_pending_engagements)
        
        # Reset daily counters at midnight
        schedule.every().day.at("00:01").do(self.reset_daily_counters)
        
        # Start the scheduler in a separate thread
        self.thread = threading.Thread(target=self._run_scheduler)
        self.thread.daemon = True
        self.thread.start()
        
        logger.info(f"Scheduler started with engagements at {morning_hour}:{morning_minute}, {midday_hour}:{midday_minute}, and {evening_hour}:{evening_minute}")
    
    def stop(self):
        """Stop the engagement scheduler."""
        if not self.running:
            logger.warning("Scheduler is not running")
            return
        
        logger.info("Stopping engagement scheduler")
        self.running = False
        
        # Clear all scheduled jobs
        schedule.clear()
        
        if self.automator:
            self.automator.close_browser()
            self.automator = None
        
        logger.info("Scheduler stopped")
    
    def process_pending_engagements(self):
        """Process pending engagement records."""
        logger.info("Processing pending engagements")
        
        # Check if we've reached the daily limit
        if self.daily_engagement_count >= self.max_engagements_per_day:
            logger.info(f"Daily engagement limit reached ({self.max_engagements_per_day}). Skipping.")
            return
        
        # Reset counters if it's a new day
        current_date = datetime.now().date()
        if current_date > self.last_reset_date:
            self.reset_daily_counters()
        
        # Get pending engagements
        remaining_capacity = self.max_engagements_per_day - self.daily_engagement_count
        pending_engagements = self.supabase.get_pending_engagements(limit=remaining_capacity)
        
        if not pending_engagements:
            logger.info("No pending engagements found")
            return
        
        logger.info(f"Found {len(pending_engagements)} pending engagements")
        
        # Initialize Instagram automator
        if not self.automator:
            self.automator = InstagramAutomator()
            
            # Start browser and login
            if not self.automator.start_browser():
                logger.error("Failed to start browser. Skipping engagements.")
                return
            
            if not self.automator.login():
                logger.error("Failed to log in to Instagram. Skipping engagements.")
                return
        
        # Process each engagement
        for engagement in pending_engagements:
            # Get the post URL from the post ID
            post_id = engagement["post_id"]
            post_data = self.supabase.client.table("posts").select("post_url").eq("id", post_id).execute()
            
            if not post_data.data:
                logger.error(f"Post with ID {post_id} not found. Skipping engagement.")
                self.supabase.update_engagement_status(engagement["id"], "failed")
                continue
            
            post_url = post_data.data[0]["post_url"]
            
            # Process based on engagement type
            success = False
            
            if engagement["engagement_type"] == "like":
                success = self.automator.like_post(post_url)
                
            elif engagement["engagement_type"] == "comment":
                # Get the comment text
                comment_id = engagement["comment_id"]
                comment_data = self.supabase.client.table("comments").select("content").eq("id", comment_id).execute()
                
                if not comment_data.data:
                    logger.error(f"Comment with ID {comment_id} not found. Skipping engagement.")
                    self.supabase.update_engagement_status(engagement["id"], "failed")
                    continue
                
                comment_text = comment_data.data[0]["content"]
                success = self.automator.comment_on_post(post_url, comment_text)
                
            elif engagement["engagement_type"] == "follow":
                # Get the user username
                user_id = engagement["user_id"]
                user_data = self.supabase.client.table("users").select("username").eq("id", user_id).execute()
                
                if not user_data.data:
                    logger.error(f"User with ID {user_id} not found. Skipping engagement.")
                    self.supabase.update_engagement_status(engagement["id"], "failed")
                    continue
                
                username = user_data.data[0]["username"]
                success = self.automator.follow_user(username)
            
            # Update engagement status
            if success:
                self.supabase.update_engagement_status(engagement["id"], "success", datetime.utcnow().isoformat())
                self.daily_engagement_count += 1
                logger.info(f"Successfully processed {engagement['engagement_type']} engagement for post {post_id}")
            else:
                self.supabase.update_engagement_status(engagement["id"], "failed")
                logger.error(f"Failed to process {engagement['engagement_type']} engagement for post {post_id}")
            
            # Add a delay between engagements to avoid detection
            delay = random.uniform(30, 60)  # 30-60 seconds
            time.sleep(delay)
            
            # Check if we've reached the daily limit
            if self.daily_engagement_count >= self.max_engagements_per_day:
                logger.info(f"Daily engagement limit reached ({self.max_engagements_per_day}). Stopping.")
                break
        
        logger.info(f"Processed {len(pending_engagements)} engagements. Daily count: {self.daily_engagement_count}")
    
    def reset_daily_counters(self):
        """Reset daily engagement counters."""
        self.daily_engagement_count = 0
        self.last_reset_date = datetime.now().date()
        logger.info("Reset daily engagement counters")
    
    def _run_scheduler(self):
        """Run the scheduler loop."""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
