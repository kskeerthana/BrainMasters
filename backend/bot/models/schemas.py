from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid


class HashtagConfig(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    hashtag: str
    is_active: bool = True
    priority: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_scraped: Optional[datetime] = None


class InstagramUser(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    full_name: Optional[str] = None
    bio: Optional[str] = None
    follower_count: Optional[int] = None
    following_count: Optional[int] = None
    post_count: Optional[int] = None
    is_private: bool = False
    is_verified: bool = False
    last_post_date: Optional[datetime] = None
    is_influencer: bool = False
    niche_relevance_score: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def dict(self, *args, **kwargs):
        result = super().dict(*args, **kwargs)
        # Convert datetime objects to ISO format for MongoDB compatibility
        for key, value in result.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
        return result


class InstagramPost(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    shortcode: str
    owner_username: str
    caption: Optional[str] = None
    hashtags: List[str] = []
    likes_count: Optional[int] = None
    comments_count: Optional[int] = None
    post_url: str
    posted_at: Optional[datetime] = None
    is_video: bool = False
    is_engaged: bool = False
    niche_relevance_score: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    def dict(self, *args, **kwargs):
        result = super().dict(*args, **kwargs)
        # Convert datetime objects to ISO format for MongoDB compatibility
        for key, value in result.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
        return result


class Comment(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    post_id: str
    is_posted: bool = False
    posted_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class EngagementRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    post_id: str
    user_id: Optional[str] = None
    engagement_type: str  # like, comment, follow
    comment_id: Optional[str] = None
    status: str = "pending"  # pending, success, failed
    scheduled_at: Optional[datetime] = None
    executed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    def dict(self, *args, **kwargs):
        result = super().dict(*args, **kwargs)
        # Convert datetime objects to ISO format for MongoDB compatibility
        for key, value in result.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
        return result
