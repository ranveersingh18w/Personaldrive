import React from 'react';

function Stats({ stats }) {
  return (
    <div className="stats">
      <div className="stat-card">
        <h3>{stats.total_files || 0}</h3>
        <p>Total Files</p>
      </div>
      
      <div className="stat-card">
        <h3>{stats.image_count || 0}</h3>
        <p>Photos</p>
      </div>
      
      <div className="stat-card">
        <h3>{stats.video_count || 0}</h3>
        <p>Videos</p>
      </div>
      
      <div className="stat-card">
        <h3>{stats.total_size_formatted || '0 B'}</h3>
        <p>Total Size</p>
      </div>
    </div>
  );
}

export default Stats;
