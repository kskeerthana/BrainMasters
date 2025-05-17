import os
import logging
import openai
from typing import Optional, Dict, Any, List
from pathlib import Path
from dotenv import load_dotenv

# Import our models
from ..models.schemas import InstagramPost, InstagramUser, Comment

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent.parent
load_dotenv(ROOT_DIR / '.env')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CommentGenerator:
    def __init__(self):
        # Set up OpenAI API
        api_key = os.environ.get("OPENAI_API_KEY")
        
        if not api_key or api_key == "your_openai_api_key":
            logger.warning("OpenAI API key not set or is a placeholder.")
            self.client = None
        else:
            try:
                self.client = openai.OpenAI(api_key=api_key)
                logger.info("Successfully initialized OpenAI client")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {str(e)}")
                self.client = None
    
    def _is_configured(self):
        """Check if the OpenAI client is properly configured."""
        return self.client is not None
    
    def generate_post_comment(self, post: InstagramPost) -> Optional[str]:
        """
        Generate a personalized comment for an Instagram post.
        
        Args:
            post: The Instagram post to comment on
            
        Returns:
            A generated comment or None if generation failed
        """
        if not self._is_configured():
            logger.error("OpenAI client not configured. Cannot generate comment.")
            return None
        
        try:
            # Extract post information for context
            post_info = {
                "username": post.owner_username,
                "caption": post.caption if post.caption else "",
                "hashtags": post.hashtags
            }
            
            # Create prompt
            prompt = self._create_post_comment_prompt(post_info)
            
            # Generate response
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an Instagram engagement specialist who writes authentic, personalized comments. Your comments are thoughtful, specific to the content, and designed to start meaningful conversations. Avoid generic statements like 'nice post' or too many emojis. Your comments should be 1-3 sentences maximum and focused on the specific post content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            # Extract the generated comment
            comment_text = response.choices[0].message.content.strip()
            logger.info(f"Generated comment for post {post.shortcode}")
            
            return comment_text
            
        except Exception as e:
            logger.error(f"Error generating comment for post {post.shortcode}: {str(e)}")
            return None
    
    def generate_user_comment(self, user: InstagramUser, user_post: InstagramPost) -> Optional[str]:
        """
        Generate a personalized comment for a user's post.
        
        Args:
            user: The Instagram user whose post we're commenting on
            user_post: The user's post to comment on
            
        Returns:
            A generated comment or None if generation failed
        """
        if not self._is_configured():
            logger.error("OpenAI client not configured. Cannot generate comment.")
            return None
        
        try:
            # Extract user and post information for context
            context = {
                "username": user.username,
                "full_name": user.full_name if user.full_name else "",
                "bio": user.bio if user.bio else "",
                "is_influencer": user.is_influencer,
                "post_caption": user_post.caption if user_post.caption else "",
                "post_hashtags": user_post.hashtags
            }
            
            # Create prompt
            prompt = self._create_user_comment_prompt(context)
            
            # Generate response
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an Instagram engagement specialist who writes authentic, personalized comments. Your comments are thoughtful, specific to the content, and designed to start meaningful conversations. Avoid generic statements like 'nice post' or too many emojis. Your comments should be 1-3 sentences maximum and focused on the specific post content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            # Extract the generated comment
            comment_text = response.choices[0].message.content.strip()
            logger.info(f"Generated comment for user {user.username}'s post")
            
            return comment_text
            
        except Exception as e:
            logger.error(f"Error generating comment for user {user.username}'s post: {str(e)}")
            return None
    
    def _create_post_comment_prompt(self, post_info: Dict[str, Any]) -> str:
        """Create a prompt for generating a comment on a hashtag post."""
        prompt = f"""
        Generate a personalized, thoughtful comment for an Instagram post by {post_info['username']}.
        
        Post caption: "{post_info['caption']}"
        
        Hashtags: {', '.join(['#' + tag for tag in post_info['hashtags']])}
        
        Your comment should:
        1. Be specific to the content shown in the caption
        2. Include a genuine compliment or observation
        3. End with a thoughtful question to encourage response
        4. Be between 1-3 sentences in length
        5. Sound natural and conversational
        6. Avoid generic phrases like "nice post" or "great content"
        
        Write only the comment text with no additional explanations or quotes.
        """
        return prompt
    
    def _create_user_comment_prompt(self, context: Dict[str, Any]) -> str:
        """Create a prompt for generating a comment on a user's post."""
        influencer_context = "This person appears to be an influencer in their niche." if context['is_influencer'] else ""
        
        prompt = f"""
        Generate a personalized, thoughtful comment for an Instagram post by {context['username']}.
        
        User information:
        - Username: {context['username']}
        - Name: {context['full_name']}
        - Bio: "{context['bio']}"
        {influencer_context}
        
        Post caption: "{context['post_caption']}"
        
        Hashtags: {', '.join(['#' + tag for tag in context['post_hashtags']])}
        
        Your comment should:
        1. Be specific to the content shown in the post caption
        2. Reference something from their bio if relevant
        3. Include a genuine compliment or observation
        4. End with a thoughtful question to encourage response
        5. Be between 1-3 sentences in length
        6. Sound natural and conversational
        7. Avoid generic phrases like "nice post" or "great content"
        
        Write only the comment text with no additional explanations or quotes.
        """
        return prompt
