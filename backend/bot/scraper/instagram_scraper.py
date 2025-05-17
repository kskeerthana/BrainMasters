import os
import logging
import instaloader
from instaloader.exceptions import LoginRequiredException, ConnectionException
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

# Import our models
from ..models.schemas import InstagramPost, InstagramUser

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent.parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class InstagramScraper:
    def __init__(self):
        self.L = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=True,
            save_metadata=False,
            compress_json=False
        )
        
        # Try to login if credentials are available
        self._try_login()
    
    def _try_login(self):
        """Attempt to login to Instagram using credentials from environment variables."""
        username = os.environ.get("INSTAGRAM_USERNAME")
        password = os.environ.get("INSTAGRAM_PASSWORD")
        
        if not username or not password or username == "your_username" or password == "your_password":
            logger.warning("Instagram credentials not set or are placeholders. Running in anonymous mode.")
            return
        
        try:
            self.L.login(username, password)
            logger.info(f"Successfully logged in as {username}")
        except Exception as e:
            logger.error(f"Failed to login to Instagram: {str(e)}")
    
    def get_hashtag_posts(self, hashtag: str, max_posts: int = 10) -> List[InstagramPost]:
        """
        Retrieve recent posts from a specific hashtag.
        
        Args:
            hashtag: The hashtag to scrape (without the # symbol)
            max_posts: Maximum number of posts to retrieve
            
        Returns:
            List of InstagramPost objects
        """
        logger.info(f"Scraping posts for hashtag: #{hashtag}")
        hashtag_clean = hashtag.replace("#", "")
        
        try:
            hashtag_obj = instaloader.Hashtag.from_name(self.L.context, hashtag_clean)
            posts = []
            
            for post in hashtag_obj.get_posts():
                if len(posts) >= max_posts:
                    break
                
                # Extract hashtags from caption
                hashtags = []
                if post.caption:
                    hashtags = [tag.strip("#") for tag in post.caption.split() if tag.startswith("#")]
                
                # Create InstagramPost object
                post_obj = InstagramPost(
                    shortcode=post.shortcode,
                    owner_username=post.owner_username,
                    caption=post.caption,
                    hashtags=hashtags,
                    likes_count=post.likes,
                    comments_count=post.comments,
                    post_url=f"https://www.instagram.com/p/{post.shortcode}/",
                    posted_at=post.date_utc,
                    is_video=post.is_video
                )
                
                posts.append(post_obj)
                logger.debug(f"Scraped post {post.shortcode} by {post.owner_username}")
            
            logger.info(f"Successfully scraped {len(posts)} posts for #{hashtag_clean}")
            return posts
            
        except ConnectionException as e:
            logger.error(f"Connection error while scraping #{hashtag_clean}: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error scraping #{hashtag_clean}: {str(e)}")
            return []
    
    def get_post_commenters(self, post: InstagramPost, min_followers: int = 100) -> List[InstagramUser]:
        """
        Extract users who commented on a post and retrieve their metadata.
        
        Args:
            post: The InstagramPost to analyze
            min_followers: Minimum follower count for users to include
            
        Returns:
            List of InstagramUser objects
        """
        logger.info(f"Extracting commenters from post {post.shortcode}")
        commenters = []
        
        try:
            post_obj = instaloader.Post.from_shortcode(self.L.context, post.shortcode)
            
            # Get comments
            comments = post_obj.get_comments()
            
            # Track unique commenters to avoid duplicates
            unique_commenters = set()
            
            for comment in comments:
                username = comment.owner.username
                
                # Skip if we've already processed this user
                if username in unique_commenters:
                    continue
                
                unique_commenters.add(username)
                
                try:
                    # Get user profile
                    profile = instaloader.Profile.from_username(self.L.context, username)
                    
                    # Skip if below minimum follower threshold
                    if profile.followers < min_followers:
                        continue
                    
                    # Determine if the user is an "influencer" based on follower count
                    min_influencer_followers = int(os.environ.get("MIN_FOLLOWER_COUNT_INFLUENCER", 500))
                    is_influencer = profile.followers >= min_influencer_followers
                    
                    # Get date of most recent post
                    last_post_date = None
                    try:
                        for post in profile.get_posts():
                            last_post_date = post.date_utc
                            break  # We just need the first/most recent post
                    except:
                        pass
                    
                    # Create user object
                    user = InstagramUser(
                        username=username,
                        full_name=profile.full_name,
                        bio=profile.biography,
                        follower_count=profile.followers,
                        following_count=profile.followees,
                        post_count=profile.mediacount,
                        is_private=profile.is_private,
                        is_verified=profile.is_verified,
                        last_post_date=last_post_date,
                        is_influencer=is_influencer
                    )
                    
                    commenters.append(user)
                    logger.debug(f"Extracted commenter: {username}")
                    
                except Exception as e:
                    logger.warning(f"Could not extract data for commenter {username}: {str(e)}")
            
            logger.info(f"Extracted {len(commenters)} commenters from post {post.shortcode}")
            return commenters
            
        except Exception as e:
            logger.error(f"Error extracting commenters from post {post.shortcode}: {str(e)}")
            return []
