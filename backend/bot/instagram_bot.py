import os
import logging
import asyncio
import time
from typing import List, Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Import our modules
from .scraper import InstagramScraper
from .gpt import CommentGenerator
from .automation import InstagramAutomator
from .scheduler import EngagementScheduler
from .utils import filter_users_by_relevance, filter_posts_by_relevance
from .models.schemas import HashtagConfig, InstagramPost, InstagramUser, EngagementRecord, Comment
from .db.supabase_client import SupabaseClient
from .db.mongo_client import MongoClient

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class InstagramBot:
    def __init__(self):
        """Initialize the Instagram engagement bot."""
        self.scraper = InstagramScraper()
        self.comment_generator = CommentGenerator()
        self.scheduler = EngagementScheduler()
        self.supabase = SupabaseClient()
        self.mongo = MongoClient()
        
        # Load configuration
        self.max_posts_per_hashtag = int(os.environ.get("MAX_POSTS_PER_HASHTAG", 10))
        self.min_follower_count = int(os.environ.get("MIN_FOLLOWER_COUNT_REGULAR", 100))
        self.target_hashtags = os.environ.get("TARGET_HASHTAGS", "").replace("#", "").split(",")
        
        # Clean and normalize hashtags
        self.target_hashtags = [tag.strip() for tag in self.target_hashtags if tag.strip()]
        
        logger.info(f"Instagram bot initialized with target hashtags: {', '.join(['#' + tag for tag in self.target_hashtags])}")
    
    async def run_scraping_job(self):
        """Run a full scraping job for all target hashtags."""
        logger.info("Starting hashtag scraping job")
        
        for hashtag in self.target_hashtags:
            logger.info(f"Processing hashtag: #{hashtag}")
            
            # Scrape posts for hashtag
            posts = self.scraper.get_hashtag_posts(hashtag, max_posts=self.max_posts_per_hashtag)
            
            if not posts:
                logger.warning(f"No posts found for hashtag: #{hashtag}")
                continue
            
            logger.info(f"Found {len(posts)} posts for hashtag: #{hashtag}")
            
            # Filter posts by relevance
            relevant_posts = filter_posts_by_relevance(posts, self.target_hashtags)
            logger.info(f"Filtered down to {len(relevant_posts)} relevant posts")
            
            # Save posts to database
            for post in relevant_posts:
                await self.mongo.save_post(post)
                
                # Generate and save comment for this post
                await self._generate_comment_for_post(post)
                
                # Extract commenters
                commenters = self.scraper.get_post_commenters(post, min_followers=self.min_follower_count)
                
                if not commenters:
                    logger.warning(f"No qualifying commenters found for post {post.shortcode}")
                    continue
                
                logger.info(f"Found {len(commenters)} commenters for post {post.shortcode}")
                
                # Filter users by relevance
                relevant_users = filter_users_by_relevance(commenters, self.target_hashtags)
                logger.info(f"Filtered down to {len(relevant_users)} relevant users")
                
                # Save users to database
                for user in relevant_users:
                    await self.mongo.save_user(user)
                    
                    # Schedule engagement with this user
                    await self._schedule_user_engagement(user, post)
            
            logger.info(f"Completed processing for hashtag: #{hashtag}")
            
        logger.info("Hashtag scraping job completed")
    
    async def _generate_comment_for_post(self, post: InstagramPost):
        """Generate and save a comment for a post."""
        # Generate comment using GPT
        comment_text = self.comment_generator.generate_post_comment(post)
        
        if not comment_text:
            logger.warning(f"Failed to generate comment for post {post.shortcode}")
            return
        
        # Create comment record
        comment = Comment(
            content=comment_text,
            post_id=post.id
        )
        
        # Save to database
        comment_id = await self.mongo.save_comment(comment)
        logger.info(f"Saved comment for post {post.shortcode}: {comment_id}")
        
        # Schedule engagement record for this comment
        engagement = EngagementRecord(
            post_id=post.id,
            engagement_type="comment",
            comment_id=comment.id,
            scheduled_at=datetime.utcnow()
        )
        
        await self.mongo.save_engagement(engagement)
        logger.info(f"Scheduled comment engagement for post {post.shortcode}")
    
    async def _schedule_user_engagement(self, user: InstagramUser, original_post: InstagramPost):
        """Schedule engagement with a user."""
        # First, schedule a follow engagement
        follow_engagement = EngagementRecord(
            user_id=user.id,
            post_id=original_post.id,  # Reference for tracking
            engagement_type="follow",
            scheduled_at=datetime.utcnow()
        )
        
        await self.mongo.save_engagement(follow_engagement)
        logger.info(f"Scheduled follow engagement for user {user.username}")
        
        # TODO: In a full implementation, we would:
        # 1. Scrape recent posts from this user
        # 2. Generate comments for those posts
        # 3. Schedule like and comment engagements
    
    def start_scheduler(self):
        """Start the engagement scheduler."""
        self.scheduler.start()
        logger.info("Engagement scheduler started")
    
    def stop_scheduler(self):
        """Stop the engagement scheduler."""
        self.scheduler.stop()
        logger.info("Engagement scheduler stopped")

    async def get_stats(self):
        """Get bot statistics."""
        # Get user stats
        user_stats = await self.mongo.get_user_stats()
        
        # Get engagement stats
        engagement_stats = await self.mongo.get_engagement_stats()
        
        # Combine stats
        stats = {
            "user_stats": user_stats,
            "engagement_stats": engagement_stats,
            "hashtags": self.target_hashtags,
            "configuration": {
                "max_posts_per_hashtag": self.max_posts_per_hashtag,
                "min_follower_count": self.min_follower_count
            }
        }
        
        return stats
