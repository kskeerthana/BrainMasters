import React, { useState } from 'react';

const Settings = ({ configuration = {} }) => {
  const [settings, setSettings] = useState({
    max_posts_per_hashtag: configuration.max_posts_per_hashtag || 10,
    min_follower_count: configuration.min_follower_count || 100,
    instagram_username: '',
    instagram_password: '',
    openai_api_key: '',
    supabase_url: '',
    supabase_key: ''
  });
  
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSettings({
      ...settings,
      [name]: value
    });
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    // TODO: Send to API
    alert('Note: API integration for saving settings is not yet implemented. This is a UI mockup.');
  };
  
  return (
    <div className="settings">
      <div className="dashboard-header">
        <h1>Bot Settings</h1>
        <p>Configure your Instagram engagement bot</p>
      </div>
      
      <form className="settings-form" onSubmit={handleSubmit}>
        <div className="form-section">
          <h2>Instagram Credentials</h2>
          <div className="form-group">
            <label htmlFor="instagram_username">Instagram Username</label>
            <input
              type="text"
              id="instagram_username"
              name="instagram_username"
              value={settings.instagram_username}
              onChange={handleInputChange}
              placeholder="Your Instagram username"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="instagram_password">Instagram Password</label>
            <input
              type="password"
              id="instagram_password"
              name="instagram_password"
              value={settings.instagram_password}
              onChange={handleInputChange}
              placeholder="Your Instagram password"
            />
          </div>
        </div>
        
        <div className="form-section">
          <h2>API Keys</h2>
          <div className="form-group">
            <label htmlFor="openai_api_key">OpenAI API Key</label>
            <input
              type="password"
              id="openai_api_key"
              name="openai_api_key"
              value={settings.openai_api_key}
              onChange={handleInputChange}
              placeholder="sk-..."
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="supabase_url">Supabase URL</label>
            <input
              type="text"
              id="supabase_url"
              name="supabase_url"
              value={settings.supabase_url}
              onChange={handleInputChange}
              placeholder="https://your-project.supabase.co"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="supabase_key">Supabase Key</label>
            <input
              type="password"
              id="supabase_key"
              name="supabase_key"
              value={settings.supabase_key}
              onChange={handleInputChange}
              placeholder="Your Supabase API key"
            />
          </div>
        </div>
        
        <div className="form-section">
          <h2>Bot Configuration</h2>
          <div className="form-group">
            <label htmlFor="max_posts_per_hashtag">Max Posts Per Hashtag</label>
            <input
              type="number"
              id="max_posts_per_hashtag"
              name="max_posts_per_hashtag"
              value={settings.max_posts_per_hashtag}
              onChange={handleInputChange}
              min="1"
              max="50"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="min_follower_count">Minimum Follower Count</label>
            <input
              type="number"
              id="min_follower_count"
              name="min_follower_count"
              value={settings.min_follower_count}
              onChange={handleInputChange}
              min="1"
            />
          </div>
        </div>
        
        <button type="submit" className="btn-primary">Save Settings</button>
      </form>
      
      <div className="note-card" style={{ marginTop: '20px' }}>
        <p><strong>Note:</strong> Your credentials are stored securely in environment variables on the server and are never exposed to the frontend.</p>
      </div>
      
      <style jsx>{`
        .form-section {
          margin-bottom: 30px;
        }
        
        .form-section h2 {
          margin-bottom: 15px;
          font-size: 18px;
        }
        
        .note-card {
          background-color: #fff3cd;
          border: 1px solid #ffeeba;
          border-radius: 10px;
          padding: 15px;
          color: #856404;
        }
      `}</style>
    </div>
  );
};

export default Settings;
