import React from 'react';

const Dashboard = ({ stats }) => {
  const { user_stats, engagement_stats } = stats;
  
  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Instagram Engagement Dashboard</h1>
        <p>Monitor your bot's performance and analytics</p>
      </div>
      
      <img 
        src="https://images.unsplash.com/photo-1666875753105-c63a6f3bdc86" 
        alt="Analytics Dashboard" 
        className="dashboard-image" 
      />
      
      <div className="stats-grid">
        <div className="stat-card">
          <h2>{user_stats.total_users || 0}</h2>
          <p>Total Users Tracked</p>
        </div>
        
        <div className="stat-card">
          <h2>{user_stats.engaged_users || 0}</h2>
          <p>Users Engaged</p>
        </div>
        
        <div className="stat-card">
          <h2>{user_stats.influencers || 0}</h2>
          <p>Influencers Found</p>
        </div>
        
        <div className="stat-card">
          <h2>{engagement_stats.reduce((sum, item) => sum + (item.successful || 0), 0)}</h2>
          <p>Successful Engagements</p>
        </div>
      </div>
      
      <div className="dashboard-section">
        <h2>Engagement Breakdown</h2>
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
            {engagement_stats.map((item, index) => {
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
            {engagement_stats.length === 0 && (
              <tr>
                <td colSpan="5" style={{ textAlign: 'center' }}>No engagement data available</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;
