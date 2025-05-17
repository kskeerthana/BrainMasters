import logging
import re
from typing import List, Dict, Any
import random

# Import models
from ..models.schemas import InstagramPost, InstagramUser

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def filter_users_by_relevance(users: List[InstagramUser], hashtags: List[str], min_score: float = 0.3) -> List[InstagramUser]:
    """
    Filter users by relevance to target hashtags.
    
    Args:
        users: List of InstagramUser objects to filter
        hashtags: List of target hashtags (without # symbol)
        min_score: Minimum relevance score (0-1)
        
    Returns:
        Filtered list of users
    """
    logger.info(f"Filtering {len(users)} users by relevance to {len(hashtags)} hashtags")
    
    relevant_users = []
    
    for user in users:
        # Skip private accounts
        if user.is_private:
            continue
        
        # Skip accounts with no bio
        if not user.bio:
            continue
        
        # Calculate relevance score
        score = _calculate_user_relevance(user, hashtags)
        
        # Update user with score
        user.niche_relevance_score = score
        
        # Include if above threshold
        if score >= min_score:
            relevant_users.append(user)
    
    logger.info(f"Found {len(relevant_users)} relevant users with score >= {min_score}")
    return relevant_users

def filter_posts_by_relevance(posts: List[InstagramPost], hashtags: List[str], min_score: float = 0.3) -> List[InstagramPost]:
    """
    Filter posts by relevance to target hashtags.
    
    Args:
        posts: List of InstagramPost objects to filter
        hashtags: List of target hashtags (without # symbol)
        min_score: Minimum relevance score (0-1)
        
    Returns:
        Filtered list of posts
    """
    logger.info(f"Filtering {len(posts)} posts by relevance to {len(hashtags)} hashtags")
    
    relevant_posts = []
    
    for post in posts:
        # Skip posts with no caption
        if not post.caption:
            continue
        
        # Calculate relevance score
        score = _calculate_post_relevance(post, hashtags)
        
        # Update post with score
        post.niche_relevance_score = score
        
        # Include if above threshold
        if score >= min_score:
            relevant_posts.append(post)
    
    logger.info(f"Found {len(relevant_posts)} relevant posts with score >= {min_score}")
    return relevant_posts

def _calculate_user_relevance(user: InstagramUser, hashtags: List[str]) -> float:
    """Calculate the relevance score of a user based on their bio and other metadata."""
    
    # Base score
    score = 0.0
    max_score = 1.0
    
    # Check if bio contains any target hashtags or keywords
    if user.bio:
        bio_lower = user.bio.lower()
        
        # Count hashtag matches
        hashtag_matches = 0
        for tag in hashtags:
            # Check for exact hashtag match
            if f"#{tag.lower()}" in bio_lower:
                hashtag_matches += 1
            # Check for keyword match without hashtag
            elif tag.lower() in bio_lower:
                hashtag_matches += 0.5
        
        # Calculate hashtag relevance (max 0.5)
        if hashtags:
            hashtag_score = 0.5 * (hashtag_matches / len(hashtags))
            score += hashtag_score
    
    # Account quality factors (max 0.5)
    quality_score = 0.0
    
    # Verified accounts get a boost
    if user.is_verified:
        quality_score += 0.1
    
    # Active accounts get a boost (posted recently)
    if user.last_post_date:
        quality_score += 0.1
    
    # Influencer status gets a boost
    if user.is_influencer:
        quality_score += 0.1
    
    # Account with good following/follower ratio
    if user.follower_count and user.following_count:
        if user.follower_count > user.following_count:
            quality_score += 0.1
    
    # Add random factor for diversity (0-0.1)
    quality_score += random.uniform(0, 0.1)
    
    # Cap quality score at 0.5
    quality_score = min(0.5, quality_score)
    score += quality_score
    
    return min(max_score, score)

def _calculate_post_relevance(post: InstagramPost, hashtags: List[str]) -> float:
    """Calculate the relevance score of a post based on its caption, hashtags, and metadata."""
    
    # Base score
    score = 0.0
    max_score = 1.0
    
    # Check hashtag overlap
    hashtag_score = 0.0
    if post.hashtags and hashtags:
        # Normalize hashtags for comparison
        post_tags = [tag.lower() for tag in post.hashtags]
        target_tags = [tag.lower() for tag in hashtags]
        
        # Count matches
        matches = sum(1 for tag in post_tags if tag in target_tags)
        
        # Calculate overlap score (max 0.6)
        if matches > 0:
            hashtag_score = 0.6 * (matches / len(target_tags))
    
    score += hashtag_score
    
    # Caption relevance (max 0.3)
    caption_score = 0.0
    if post.caption and hashtags:
        caption_lower = post.caption.lower()
        
        # Count keyword matches in caption
        keyword_matches = sum(1 for tag in hashtags if tag.lower() in caption_lower)
        
        if keyword_matches > 0:
            caption_score = 0.3 * (keyword_matches / len(hashtags))
    
    score += caption_score
    
    # Engagement quality (max 0.1)
    engagement_score = 0.0
    
    # Posts with higher engagement get a boost
    if post.likes_count and post.comments_count:
        # Simple engagement rate calculation
        engagement = post.likes_count + post.comments_count
        
        # Scale based on typical engagement levels
        if engagement > 1000:
            engagement_score = 0.1
        elif engagement > 500:
            engagement_score = 0.08
        elif engagement > 100:
            engagement_score = 0.05
        elif engagement > 50:
            engagement_score = 0.03
        else:
            engagement_score = 0.01
    
    score += engagement_score
    
    return min(max_score, score)
