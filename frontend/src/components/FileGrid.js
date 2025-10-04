import React from 'react';

function FileGrid({ files, onDelete, apiUrl }) {
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    if (bytes < 1024 * 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
    return (bytes / (1024 * 1024 * 1024)).toFixed(2) + ' GB';
  };

  const handleDownload = async (file) => {
    try {
      const response = await fetch(`${apiUrl}/file/${file.id}`);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = file.original_filename;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Download error:', error);
      alert('Failed to download file');
    }
  };

  if (files.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">📁</div>
        <h2>No files yet</h2>
        <p>Upload some photos or videos to get started!</p>
      </div>
    );
  }

  return (
    <div className="file-grid">
      {files.map((file) => (
        <div key={file.id} className="file-card">
          {file.file_type === 'image' && file.thumbnail_path ? (
            <img
              src={`${apiUrl}/thumbnail/${file.id}`}
              alt={file.original_filename}
              className="file-thumbnail"
            />
          ) : (
            <div className="file-placeholder">
              {file.file_type === 'image' ? '🖼️' : '🎥'}
            </div>
          )}

          <div className="file-info">
            <h3 className="file-name" title={file.original_filename}>
              {file.original_filename}
            </h3>
            
            <div className="file-meta">
              <div>📅 {formatDate(file.upload_date)}</div>
              <div>💾 {formatFileSize(file.file_size)}</div>
              {file.width && file.height && (
                <div>📐 {file.width} × {file.height}</div>
              )}
            </div>

            <div className="file-actions">
              <button
                className="btn-download"
                onClick={() => handleDownload(file)}
              >
                ⬇️ Download
              </button>
              <button
                className="btn-delete"
                onClick={() => onDelete(file.id)}
              >
                🗑️ Delete
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default FileGrid;
