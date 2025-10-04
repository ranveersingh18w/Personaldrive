import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import FileUpload from './components/FileUpload';
import FileGrid from './components/FileGrid';
import Stats from './components/Stats';
import SearchBar from './components/SearchBar';

// Use environment variable for API URL (for Vercel deployment)
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [files, setFiles] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState('all');

  const fetchFiles = async () => {
    try {
      setLoading(true);
      const params = {};
      if (filterType !== 'all') {
        params.type = filterType;
      }
      
      const response = await axios.get(`${API_URL}/files`, { params });
      setFiles(response.data.files);
    } catch (error) {
      console.error('Error fetching files:', error);
      if (error.code === 'ERR_NETWORK') {
        console.log('Backend server not running. Please start the backend first.');
      }
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_URL}/stats`);
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  useEffect(() => {
    fetchFiles();
    fetchStats();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filterType]);

  const handleSearch = async (query) => {
    
    if (!query.trim()) {
      fetchFiles();
      return;
    }
    
    try {
      setLoading(true);
      const response = await axios.get(`${API_URL}/search`, {
        params: { q: query }
      });
      setFiles(response.data.files);
    } catch (error) {
      console.error('Error searching files:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadComplete = () => {
    fetchFiles();
    fetchStats();
  };

  const handleDelete = async (fileId) => {
    if (!window.confirm('Are you sure you want to delete this file?')) {
      return;
    }

    try {
      await axios.delete(`${API_URL}/file/${fileId}`);
      fetchFiles();
      fetchStats();
    } catch (error) {
      console.error('Error deleting file:', error);
      alert('Failed to delete file');
    }
  };

  return (
    <div className="App">
      <header className="header">
        <div className="container">
          <h1>☁️ Personal Cloud Storage</h1>
          <p className="subtitle">Your photos and videos, safely backed up</p>
        </div>
      </header>

      <main className="container">
        {stats && <Stats stats={stats} />}

        <FileUpload onUploadComplete={handleUploadComplete} apiUrl={API_URL} />

        <div className="controls">
          <SearchBar onSearch={handleSearch} />
          
          <div className="filter-tabs">
            <button
              className={filterType === 'all' ? 'active' : ''}
              onClick={() => setFilterType('all')}
            >
              All
            </button>
            <button
              className={filterType === 'image' ? 'active' : ''}
              onClick={() => setFilterType('image')}
            >
              📷 Images
            </button>
            <button
              className={filterType === 'video' ? 'active' : ''}
              onClick={() => setFilterType('video')}
            >
              🎥 Videos
            </button>
          </div>
        </div>

        {loading ? (
          <div className="loading">
            <div className="spinner"></div>
            <p>Loading files...</p>
          </div>
        ) : (
          <FileGrid
            files={files}
            onDelete={handleDelete}
            apiUrl={API_URL}
          />
        )}
      </main>

      <footer className="footer">
        <p>Personal Cloud Storage © 2025</p>
      </footer>
    </div>
  );
}

export default App;
