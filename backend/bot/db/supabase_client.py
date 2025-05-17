import os
from dotenv import load_dotenv
from supabase import create_client, Client
from pathlib import Path

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent.parent
load_dotenv(ROOT_DIR / '.env')

class SupabaseClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
            supabase_url = os.environ.get("SUPABASE_URL")
            supabase_key = os.environ.get("SUPABASE_KEY")
            
            if not supabase_url or not supabase_key:
                raise ValueError("Supabase URL and Key must be provided in environment variables")
            
            cls._instance.client = create_client(supabase_url, supabase_key)
        return cls._instance
    
    def get_hashtags(self):
        """Retrieve all active hashtags for scraping."""
        response = self.client.table("hashtags").select("*").eq("is_active", True).execute()
        return response.data
    
    def save_post(self, post_data):
        """Save instagram post data to Supabase."""
        response = self.client.table("posts").insert(post_data).execute()
        return response.data
    
    def save_user(self, user_data):
        """Save instagram user data to Supabase."""
        # Check if user exists
        existing = self.client.table("users").select("id").eq("username", user_data["username"]).execute()
        
        if existing.data:
            # Update existing user
            user_id = existing.data[0]["id"]
            response = self.client.table("users").update(user_data).eq("id", user_id).execute()
        else:
            # Insert new user
            response = self.client.table("users").insert(user_data).execute()
            
        return response.data
    
    def save_comment(self, comment_data):
        """Save generated comment to Supabase."""
        response = self.client.table("comments").insert(comment_data).execute()
        return response.data
    
    def save_engagement(self, engagement_data):
        """Save engagement record to Supabase."""
        response = self.client.table("engagements").insert(engagement_data).execute()
        return response.data
    
    def update_engagement_status(self, engagement_id, status, executed_at=None):
        """Update the status of an engagement record."""
        data = {"status": status}
        if executed_at:
            data["executed_at"] = executed_at
            
        response = self.client.table("engagements").update(data).eq("id", engagement_id).execute()
        return response.data
    
    def get_pending_engagements(self, limit=10):
        """Get pending engagement records for processing."""
        response = self.client.table("engagements").select("*").eq("status", "pending").limit(limit).execute()
        return response.data
    
    def get_user_stats(self):
        """Get user engagement statistics."""
        query = """
        SELECT 
            COUNT(*) as total_users,
            COUNT(CASE WHEN is_engaged = true THEN 1 END) as engaged_users,
            COUNT(CASE WHEN is_influencer = true THEN 1 END) as influencers
        FROM users
        """
        response = self.client.rpc("run_query", {"query": query}).execute()
        return response.data
    
    def get_engagement_stats(self):
        """Get engagement statistics."""
        query = """
        SELECT 
            engagement_type,
            COUNT(*) as count,
            COUNT(CASE WHEN status = 'success' THEN 1 END) as successful,
            COUNT(CASE WHEN status = 'failed' THEN 1 END) as failed
        FROM engagements
        GROUP BY engagement_type
        """
        response = self.client.rpc("run_query", {"query": query}).execute()
        return response.data
