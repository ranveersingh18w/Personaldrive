"""
Database operations for file metadata storage
"""
import sqlite3
import os
from datetime import datetime
from config import DATABASE_PATH


class Database:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def init_db(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                original_filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                file_type TEXT NOT NULL,
                mime_type TEXT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_date TIMESTAMP,
                thumbnail_path TEXT,
                width INTEGER,
                height INTEGER,
                duration INTEGER,
                checksum TEXT
            )
        ''')
        
        # Create index for faster searches
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_upload_date 
            ON files(upload_date)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_file_type 
            ON files(file_type)
        ''')
        
        conn.commit()
        conn.close()
    
    def add_file(self, file_data):
        """
        Add a new file record
        
        Args:
            file_data (dict): File metadata
        
        Returns:
            int: ID of inserted record
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO files (
                filename, original_filename, file_path, file_size,
                file_type, mime_type, created_date, thumbnail_path,
                width, height, duration, checksum
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            file_data.get('filename'),
            file_data.get('original_filename'),
            file_data.get('file_path'),
            file_data.get('file_size'),
            file_data.get('file_type'),
            file_data.get('mime_type'),
            file_data.get('created_date'),
            file_data.get('thumbnail_path'),
            file_data.get('width'),
            file_data.get('height'),
            file_data.get('duration'),
            file_data.get('checksum')
        ))
        
        file_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return file_id
    
    def get_all_files(self, limit=None, offset=0, file_type=None, order_by='upload_date DESC'):
        """
        Get all files with optional filtering
        
        Args:
            limit (int): Maximum number of records to return
            offset (int): Number of records to skip
            file_type (str): Filter by file type ('image' or 'video')
            order_by (str): Sort order
        
        Returns:
            list: List of file records as dictionaries
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = 'SELECT * FROM files'
        params = []
        
        if file_type:
            query += ' WHERE file_type = ?'
            params.append(file_type)
        
        query += f' ORDER BY {order_by}'
        
        if limit:
            query += ' LIMIT ? OFFSET ?'
            params.extend([limit, offset])
        
        cursor.execute(query, params)
        files = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return files
    
    def get_file_by_id(self, file_id):
        """Get file by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM files WHERE id = ?', (file_id,))
        result = cursor.fetchone()
        
        conn.close()
        return dict(result) if result else None
    
    def get_file_by_checksum(self, checksum):
        """Get file by checksum (to detect duplicates)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM files WHERE checksum = ?', (checksum,))
        result = cursor.fetchone()
        
        conn.close()
        return dict(result) if result else None
    
    def delete_file(self, file_id):
        """Delete file record by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM files WHERE id = ?', (file_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def get_stats(self):
        """Get storage statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total files and size
        cursor.execute('''
            SELECT 
                COUNT(*) as total_files,
                SUM(file_size) as total_size,
                SUM(CASE WHEN file_type = 'image' THEN 1 ELSE 0 END) as image_count,
                SUM(CASE WHEN file_type = 'video' THEN 1 ELSE 0 END) as video_count
            FROM files
        ''')
        
        result = cursor.fetchone()
        stats = dict(result) if result else {}
        
        conn.close()
        return stats
    
    def search_files(self, query):
        """Search files by filename"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM files 
            WHERE original_filename LIKE ?
            ORDER BY upload_date DESC
        ''', (f'%{query}%',))
        
        files = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return files
