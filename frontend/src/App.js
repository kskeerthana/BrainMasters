import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import axios from 'axios';
import './App.css';

// Import components
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import HashtagsSettings from './components/HashtagsSettings';
import EngagementHistory from './components/EngagementHistory';
import Settings from './components/Settings';

function App() {
  // State for bot status
  const [botStatus, setBotStatus] = useState({
    status: 'checking',
    message: 'Checking bot status...'
  });
  
  // State for scheduler
  const [schedulerActive, setSchedulerActive] = useState(false);
  
  // State for bot statistics
  const [stats, setStats] = useState({
    user_stats: { total_users: 0, engaged_users: 0, influencers: 0 },
    engagement_stats: [],
    hashtags: [],
    configuration: { max_posts_per_hashtag: 0, min_follower_count: 0 }
  });
  
  // Backend URL from environment variable
  const API_URL = process.env.REACT_APP_BACKEND_URL || '';
  
  // Check bot status
  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/status`);
        setBotStatus(response.data);
      } catch (error) {
        console.error('Error checking bot status:', error);
        setBotStatus({
          status: 'offline',
          message: 'Bot appears to be offline. Please check server.'
        });
      }
    };
    
    checkStatus();
    // Poll status every 30 seconds
    const interval = setInterval(checkStatus, 30000);
    
    return () => clearInterval(interval);
  }, [API_URL]);
  
  // Load stats
  useEffect(() => {
    const loadStats = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/stats`);
        setStats(response.data);
      } catch (error) {
        console.error('Error loading stats:', error);
      }
    };
    
    loadStats();
    // Refresh stats every minute
    const interval = setInterval(loadStats, 60000);
    
    return () => clearInterval(interval);
  }, [API_URL]);
  
  // Start a scraping job
  const startScraping = async () => {
    try {
      const response = await axios.post(`${API_URL}/api/scraping/start`);
      alert(response.data.message);
    } catch (error) {
      console.error('Error starting scraping job:', error);
      alert('Failed to start scraping job. Please check server logs.');
    }
  };
  
  // Toggle scheduler
  const toggleScheduler = async () => {
    try {
      if (schedulerActive) {
        // Stop scheduler
        const response = await axios.post(`${API_URL}/api/scheduler/stop`);
        alert(response.data.message);
        setSchedulerActive(false);
      } else {
        // Start scheduler
        const response = await axios.post(`${API_URL}/api/scheduler/start`);
        alert(response.data.message);
        setSchedulerActive(true);
      }
    } catch (error) {
      console.error('Error toggling scheduler:', error);
      alert('Failed to toggle scheduler. Please check server logs.');
    }
  };

  return (
    <Router>
      <div className="app-container">
        <Sidebar />
        
        <div className="content-container">
          <div className="status-bar">
            <div className={`status-indicator ${botStatus.status === 'online' ? 'online' : 'offline'}`}></div>
            <span>Status: {botStatus.status}</span>
            <div className="status-actions">
              <button 
                className="btn-primary" 
                onClick={startScraping}
                disabled={botStatus.status !== 'online'}
              >
                Start Scraping
              </button>
              <button 
                className={`btn-${schedulerActive ? 'danger' : 'success'}`} 
                onClick={toggleScheduler}
                disabled={botStatus.status !== 'online'}
              >
                {schedulerActive ? 'Stop Scheduler' : 'Start Scheduler'}
              </button>
            </div>
          </div>
          
          <div className="main-content">
            <Routes>
              <Route path="/" element={<Dashboard stats={stats} />} />
              <Route path="/hashtags" element={<HashtagsSettings hashtags={stats.hashtags} />} />
              <Route path="/history" element={<EngagementHistory engagementStats={stats.engagement_stats} />} />
              <Route path="/settings" element={<Settings configuration={stats.configuration} />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;
