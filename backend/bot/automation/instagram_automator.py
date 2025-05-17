import os
import logging
import random
import time
from typing import Optional, List, Dict, Any
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright, Page, Browser

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent.parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class InstagramAutomator:
    def __init__(self):
        self.username = os.environ.get("INSTAGRAM_USERNAME")
        self.password = os.environ.get("INSTAGRAM_PASSWORD")
        
        if not self.username or not self.password or self.username == "your_username" or self.password == "your_password":
            logger.warning("Instagram credentials not set or are placeholders. Automation will not work.")
            self.is_configured = False
        else:
            self.is_configured = True
            
        self.browser = None
        self.page = None
        self.is_logged_in = False
    
    def _is_configured(self) -> bool:
        """Check if the automation is properly configured with Instagram credentials."""
        return self.is_configured
    
    def start_browser(self) -> bool:
        """Start the browser and initialize the page."""
        if not self._is_configured():
            logger.error("Instagram credentials not configured. Cannot start browser.")
            return False
        
        try:
            # Initialize browser
            playwright = sync_playwright().start()
            self.browser = playwright.chromium.launch(headless=True)
            self.page = self.browser.new_page()
            
            # Set user agent to avoid detection
            self.page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            
            logger.info("Browser started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error starting browser: {str(e)}")
            return False
    
    def login(self) -> bool:
        """Log in to Instagram."""
        if not self._is_configured() or not self.page:
            logger.error("Browser not started or Instagram credentials not configured. Cannot log in.")
            return False
        
        try:
            # Navigate to Instagram login page
            self.page.goto('https://www.instagram.com/accounts/login/')
            
            # Wait for page to load
            self.page.wait_for_selector('input[name="username"]')
            
            # Fill in credentials
            self.page.fill('input[name="username"]', self.username)
            self.page.fill('input[name="password"]', self.password)
            
            # Click login button
            self.page.click('button[type="submit"]')
            
            # Wait for login to complete
            try:
                # Wait for either the feed page or the security verification page
                self.page.wait_for_selector('svg[aria-label="Home"]', timeout=10000)
                self.is_logged_in = True
                logger.info(f"Successfully logged in as {self.username}")
                return True
            except:
                # Check if we hit a verification challenge
                if self.page.query_selector('input[name="verificationCode"]'):
                    logger.error("Login requires verification code. Please log in manually first.")
                    return False
                
                if self.page.query_selector('div[role="alert"]'):
                    logger.error("Login failed. Incorrect username or password.")
                    return False
                
                # Otherwise assume we're logged in
                self.is_logged_in = True
                logger.info(f"Logged in as {self.username}")
                return True
                
        except Exception as e:
            logger.error(f"Error logging in to Instagram: {str(e)}")
            return False
    
    def like_post(self, post_url: str) -> bool:
        """
        Like an Instagram post.
        
        Args:
            post_url: The URL of the post to like
            
        Returns:
            True if successful, False otherwise
        """
        if not self._is_configured() or not self.is_logged_in:
            logger.error("Not logged in to Instagram. Cannot like post.")
            return False
        
        try:
            # Navigate to post
            self.page.goto(post_url)
            
            # Wait for post to load
            self.page.wait_for_selector('article')
            
            # Check if already liked
            like_button = self.page.query_selector('svg[aria-label="Like"]')
            if not like_button:
                logger.info(f"Post {post_url} already liked")
                return True
            
            # Click like button
            like_button.click()
            
            # Add a random delay to avoid detection
            self._random_delay()
            
            logger.info(f"Successfully liked post {post_url}")
            return True
            
        except Exception as e:
            logger.error(f"Error liking post {post_url}: {str(e)}")
            return False
    
    def comment_on_post(self, post_url: str, comment_text: str) -> bool:
        """
        Comment on an Instagram post.
        
        Args:
            post_url: The URL of the post to comment on
            comment_text: The text to comment
            
        Returns:
            True if successful, False otherwise
        """
        if not self._is_configured() or not self.is_logged_in:
            logger.error("Not logged in to Instagram. Cannot comment on post.")
            return False
        
        try:
            # Navigate to post
            self.page.goto(post_url)
            
            # Wait for post to load
            self.page.wait_for_selector('article')
            
            # Click on comment textarea
            self.page.click('span[data-lexical-text="true"]')
            
            # Fill in comment
            self.page.fill('span[data-lexical-text="true"]', comment_text)
            
            # Wait a moment
            time.sleep(1)
            
            # Submit comment
            self.page.press('span[data-lexical-text="true"]', 'Enter')
            
            # Add a random delay to avoid detection
            self._random_delay()
            
            logger.info(f"Successfully commented on post {post_url}")
            return True
            
        except Exception as e:
            logger.error(f"Error commenting on post {post_url}: {str(e)}")
            return False
    
    def follow_user(self, username: str) -> bool:
        """
        Follow an Instagram user.
        
        Args:
            username: The username of the user to follow
            
        Returns:
            True if successful, False otherwise
        """
        if not self._is_configured() or not self.is_logged_in:
            logger.error("Not logged in to Instagram. Cannot follow user.")
            return False
        
        try:
            # Navigate to user profile
            self.page.goto(f'https://www.instagram.com/{username}/')
            
            # Wait for profile to load
            self.page.wait_for_selector('header')
            
            # Check if already following
            if self.page.query_selector('button:has-text("Following")') or self.page.query_selector('button:has-text("Requested")'):
                logger.info(f"Already following {username}")
                return True
            
            # Click follow button
            self.page.click('button:has-text("Follow")')
            
            # Add a random delay to avoid detection
            self._random_delay()
            
            logger.info(f"Successfully followed user {username}")
            return True
            
        except Exception as e:
            logger.error(f"Error following user {username}: {str(e)}")
            return False
    
    def close_browser(self):
        """Close the browser."""
        if self.browser:
            self.browser.close()
            logger.info("Browser closed")
    
    def _random_delay(self, min_seconds=2, max_seconds=5):
        """Add a random delay to mimic human behavior and avoid rate limits."""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
