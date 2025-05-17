import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent.parent
load_dotenv(ROOT_DIR / '.env')

class MongoClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoClient, cls).__new__(cls)
            mongo_url = os.environ.get("MONGO_URL")
            db_name = os.environ.get("DB_NAME", "instagram_bot_db")
            
            if not mongo_url:
                raise ValueError("MongoDB URL must be provided in environment variables")
            
            client = AsyncIOMotorClient(mongo_url)
            cls._instance.db = client[db_name]
            
            # Set up collections
            cls._instance.hashtags = cls._instance.db.hashtags
            cls._instance.posts = cls._instance.db.posts
            cls._instance.users = cls._instance.db.users
            cls._instance.comments = cls._instance.db.comments
            cls._instance.engagements = cls._instance.db.engagements
            
        return cls._instance
    
    async def get_hashtags(self):
        """Retrieve all active hashtags for scraping."""
        cursor = self.hashtags.find({"is_active": True})
        return await cursor.to_list(length=100)
    
    async def save_post(self, post_data):
        """Save instagram post data to MongoDB."""
        # Check if post exists by shortcode
        existing = await self.posts.find_one({"shortcode": post_data.shortcode})
        
        if existing:
            # Update existing post
            updated_data = post_data.dict()
            result = await self.posts.update_one(
                {"shortcode": post_data.shortcode},
                {"$set": updated_data}
            )
            return result.modified_count
        else:
            # Insert new post
            result = await self.posts.insert_one(post_data.dict())
            return str(result.inserted_id)
    
    async def save_user(self, user_data):
        """Save instagram user data to MongoDB."""
        # Check if user exists by username
        existing = await self.users.find_one({"username": user_data.username})
        
        if existing:
            # Update existing user
            updated_data = user_data.dict()
            result = await self.users.update_one(
                {"username": user_data.username},
                {"$set": updated_data}
            )
            return result.modified_count
        else:
            # Insert new user
            result = await self.users.insert_one(user_data.dict())
            return str(result.inserted_id)
    
    async def save_comment(self, comment_data):
        """Save generated comment to MongoDB."""
        result = await self.comments.insert_one(comment_data.dict())
        return str(result.inserted_id)
    
    async def save_engagement(self, engagement_data):
        """Save engagement record to MongoDB."""
        result = await self.engagements.insert_one(engagement_data.dict())
        return str(result.inserted_id)
    
    async def update_engagement_status(self, engagement_id, status, executed_at=None):
        """Update the status of an engagement record."""
        update_data = {"status": status}
        if executed_at:
            update_data["executed_at"] = executed_at
            
        result = await self.engagements.update_one(
            {"id": engagement_id},
            {"$set": update_data}
        )
        return result.modified_count
    
    async def get_pending_engagements(self, limit=10):
        """Get pending engagement records for processing."""
        cursor = self.engagements.find({"status": "pending"}).limit(limit)
        return await cursor.to_list(length=limit)
    
    async def get_user_stats(self):
        """Get user engagement statistics."""
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_users": {"$sum": 1},
                    "engaged_users": {
                        "$sum": {"$cond": [{"$eq": ["$is_engaged", True]}, 1, 0]}
                    },
                    "influencers": {
                        "$sum": {"$cond": [{"$eq": ["$is_influencer", True]}, 1, 0]}
                    }
                }
            }
        ]
        result = await self.users.aggregate(pipeline).to_list(length=1)
        return result[0] if result else {"total_users": 0, "engaged_users": 0, "influencers": 0}
    
    async def get_engagement_stats(self):
        """Get engagement statistics."""
        pipeline = [
            {
                "$group": {
                    "_id": "$engagement_type",
                    "count": {"$sum": 1},
                    "successful": {
                        "$sum": {"$cond": [{"$eq": ["$status", "success"]}, 1, 0]}
                    },
                    "failed": {
                        "$sum": {"$cond": [{"$eq": ["$status", "failed"]}, 1, 0]}
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "engagement_type": "$_id",
                    "count": 1,
                    "successful": 1,
                    "failed": 1
                }
            }
        ]
        return await self.engagements.aggregate(pipeline).to_list(length=10)
