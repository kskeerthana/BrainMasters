import React, { useState } from 'react';

const HashtagsSettings = ({ hashtags = [] }) => {
  const [hashtagList, setHashtagList] = useState(hashtags);
  const [newHashtag, setNewHashtag] = useState('');
  
  // Handle adding a new hashtag
  const handleAddHashtag = (e) => {
    e.preventDefault();
    
    if (!newHashtag.trim()) return;
    
    // Remove # if present
    let cleanHashtag = newHashtag.trim();
    if (cleanHashtag.startsWith('#')) {
      cleanHashtag = cleanHashtag.substring(1);
    }
    
    // Check for duplicates
    if (hashtagList.includes(cleanHashtag)) {
      alert('This hashtag already exists!');
      return;
    }
    
    // Add to list
    setHashtagList([...hashtagList, cleanHashtag]);
    setNewHashtag('');
    
    // TODO: Send to API
    alert('Note: API integration for saving hashtags is not yet implemented. This is a UI mockup.');
  };
  
  // Handle removing a hashtag
  const handleRemoveHashtag = (tagToRemove) => {
    setHashtagList(hashtagList.filter(tag => tag !== tagToRemove));
    
    // TODO: Send to API
    alert('Note: API integration for removing hashtags is not yet implemented. This is a UI mockup.');
  };
  
  return (
    <div className="hashtags-settings">
      <div className="dashboard-header">
        <h1>Hashtag Settings</h1>
        <p>Manage the hashtags your bot will track</p>
      </div>
      
      <div className="hashtags-container">
        <div className="hashtags-header">
          <h2>Current Hashtags</h2>
        </div>
        
        <div className="hashtags-list">
          {hashtagList.length > 0 ? (
            hashtagList.map((tag, index) => (
              <div className="hashtag-item" key={index}>
                #{tag}
                <svg 
                  onClick={() => handleRemoveHashtag(tag)}
                  xmlns="http://www.w3.org/2000/svg" 
                  width="16" 
                  height="16" 
                  viewBox="0 0 24 24" 
                  fill="none" 
                  stroke="currentColor" 
                  strokeWidth="2" 
                  strokeLinecap="round" 
                  strokeLinejoin="round"
                >
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </div>
            ))
          ) : (
            <p>No hashtags configured yet. Add some below!</p>
          )}
        </div>
      </div>
      
      <div className="add-hashtag-form">
        <h2>Add New Hashtag</h2>
        <form onSubmit={handleAddHashtag}>
          <div className="form-group">
            <label>Hashtag (with or without #)</label>
            <div style={{ display: 'flex' }}>
              <input 
                type="text" 
                value={newHashtag} 
                onChange={(e) => setNewHashtag(e.target.value)} 
                placeholder="Enter hashtag"
                style={{ borderRadius: '8px 0 0 8px' }}
              />
              <button 
                type="submit" 
                className="btn-primary"
                style={{ borderRadius: '0 8px 8px 0' }}
              >
                Add
              </button>
            </div>
          </div>
        </form>
      </div>
      
      <div className="hashtag-suggestions">
        <h2>Suggested Hashtags</h2>
        <p>Here are some popular hashtags in your niche:</p>
        
        <div className="hashtags-list">
          <div className="hashtag-item" onClick={() => setNewHashtag('motivation')}>
            #motivation
          </div>
          <div className="hashtag-item" onClick={() => setNewHashtag('mindset')}>
            #mindset
          </div>
          <div className="hashtag-item" onClick={() => setNewHashtag('productivity')}>
            #productivity
          </div>
          <div className="hashtag-item" onClick={() => setNewHashtag('selfimprovement')}>
            #selfimprovement
          </div>
          <div className="hashtag-item" onClick={() => setNewHashtag('success')}>
            #success
          </div>
        </div>
      </div>
    </div>
  );
};

export default HashtagsSettings;
