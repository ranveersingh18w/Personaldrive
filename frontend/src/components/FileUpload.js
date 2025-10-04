import React, { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';

function FileUpload({ onUploadComplete, apiUrl }) {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [uploadMessage, setUploadMessage] = useState('');

  const onDrop = async (acceptedFiles) => {
    if (acceptedFiles.length === 0) return;

    setUploading(true);
    setUploadMessage('');
    
    const totalFiles = acceptedFiles.length;
    let completedFiles = 0;

    for (const file of acceptedFiles) {
      try {
        const formData = new FormData();
        formData.append('file', file);

        await axios.post(`${apiUrl}/upload`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setProgress(percentCompleted);
          },
        });

        completedFiles++;
        setUploadMessage(`Uploaded ${completedFiles} of ${totalFiles} files`);
      } catch (error) {
        console.error('Upload error:', error);
        setUploadMessage(`Error uploading ${file.name}`);
      }
    }

    setUploading(false);
    setProgress(0);
    setUploadMessage(`✅ Successfully uploaded ${completedFiles} files!`);
    
    // Reset message after 3 seconds
    setTimeout(() => setUploadMessage(''), 3000);
    
    // Notify parent component
    onUploadComplete();
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
      'video/*': ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'],
    },
    multiple: true,
  });

  return (
    <div className="upload-section">
      <div
        {...getRootProps()}
        className={`upload-zone ${isDragActive ? 'drag-active' : ''}`}
      >
        <input {...getInputProps()} />
        <div className="upload-icon">📤</div>
        {isDragActive ? (
          <p><strong>Drop the files here...</strong></p>
        ) : (
          <>
            <p><strong>Drag & drop photos/videos here</strong></p>
            <p>or click to select files</p>
          </>
        )}
      </div>

      {uploading && (
        <div className="upload-progress">
          <p>Uploading... {progress}%</p>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${progress}%` }} />
          </div>
        </div>
      )}

      {uploadMessage && !uploading && (
        <div className="upload-message">
          <p>{uploadMessage}</p>
        </div>
      )}
    </div>
  );
}

export default FileUpload;
