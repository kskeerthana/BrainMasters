import React from 'react';

const EngagementHistory = ({ engagementStats = [] }) => {
  return (
    <div className="engagement-history">
      <div className="dashboard-header">
        <h1>Engagement History</h1>
        <p>View your bot's engagement activities and performance</p>
      </div>
      
      <div className="dashboard-section">
        <h2>Engagement Summary</h2>
        <table className="engagement-table">
          <thead>
            <tr>
              <th>Type</th>
              <th>Total</th>
              <th>Successful</th>
              <th>Failed</th>
              <th>Success Rate</th>
            </tr>
          </thead>
          <tbody>
            {engagementStats.map((item, index) => {
              const successRate = item.count > 0 
                ? Math.round((item.successful / item.count) * 100) 
                : 0;
                
              return (
                <tr key={index}>
                  <td>{item.engagement_type || 'Unknown'}</td>
                  <td>{item.count || 0}</td>
                  <td>{item.successful || 0}</td>
                  <td>{item.failed || 0}</td>
                  <td>{successRate}%</td>
                </tr>
              );
            })}
            {engagementStats.length === 0 && (
              <tr>
                <td colSpan="5" style={{ textAlign: 'center' }}>No engagement data available</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      
      <div className="dashboard-section">
        <h2>Recent Activity</h2>
        <div className="activity-list">
          <div className="activity-card">
            <div className="activity-icon comment">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
              </svg>
            </div>
            <div className="activity-content">
              <p>Commented on a post by <strong>user123</strong></p>
              <span className="activity-time">3 hours ago</span>
            </div>
            <div className="activity-status success">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
              </svg>
            </div>
          </div>
          
          <div className="activity-card">
            <div className="activity-icon like">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
              </svg>
            </div>
            <div className="activity-content">
              <p>Liked a post by <strong>influencer456</strong></p>
              <span className="activity-time">5 hours ago</span>
            </div>
            <div className="activity-status success">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
              </svg>
            </div>
          </div>
          
          <div className="activity-card">
            <div className="activity-icon follow">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="8.5" cy="7" r="4"></circle>
                <line x1="20" y1="8" x2="20" y2="14"></line>
                <line x1="23" y1="11" x2="17" y2="11"></line>
              </svg>
            </div>
            <div className="activity-content">
              <p>Followed <strong>creator789</strong></p>
              <span className="activity-time">Yesterday</span>
            </div>
            <div className="activity-status failed">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="15" y1="9" x2="9" y2="15"></line>
                <line x1="9" y1="9" x2="15" y2="15"></line>
              </svg>
            </div>
          </div>
        </div>
        
        <div className="note-card">
          <p><strong>Note:</strong> This is sample data for UI demonstration. Real engagement history will be displayed once the bot starts running and collecting data.</p>
        </div>
      </div>
      
      <style jsx>{`
        .activity-list {
          margin-top: 20px;
        }
        
        .activity-card {
          display: flex;
          align-items: center;
          padding: 15px;
          margin-bottom: 10px;
          background-color: #f8f9fa;
          border-radius: 10px;
        }
        
        .activity-icon {
          width: 40px;
          height: 40px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          margin-right: 15px;
        }
        
        .activity-icon.comment {
          background-color: #e1f5fe;
          color: #039be5;
        }
        
        .activity-icon.like {
          background-color: #ffebee;
          color: #e53935;
        }
        
        .activity-icon.follow {
          background-color: #e8f5e9;
          color: #43a047;
        }
        
        .activity-content {
          flex-grow: 1;
        }
        
        .activity-time {
          font-size: 12px;
          color: #6c757d;
        }
        
        .activity-status {
          width: 30px;
          height: 30px;
        }
        
        .activity-status.success {
          color: #28a745;
        }
        
        .activity-status.failed {
          color: #dc3545;
        }
        
        .note-card {
          background-color: #fff3cd;
          border: 1px solid #ffeeba;
          border-radius: 10px;
          padding: 15px;
          margin-top: 20px;
          color: #856404;
        }
      `}</style>
    </div>
  );
};

export default EngagementHistory;
