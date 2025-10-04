"""
Personal Cloud Storage - Client Uploader
Monitors a folder and automatically uploads new photos/videos to the server
"""
import os
import time
import requests
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import config


class FileUploader:
    def __init__(self, server_url, auth_token=None):
        self.server_url = server_url
        self.auth_token = auth_token
        self.uploaded_files = set()
        self.failed_files = {}
        
        # Load previously uploaded files from log
        self.load_uploaded_log()
    
    def load_uploaded_log(self):
        """Load list of previously uploaded files"""
        log_file = 'uploaded_files.log'
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                self.uploaded_files = set(line.strip() for line in f)
    
    def save_uploaded_log(self, file_path):
        """Save uploaded file to log"""
        with open('uploaded_files.log', 'a') as f:
            f.write(f"{file_path}\n")
    
    def upload_file(self, file_path):
        """
        Upload a file to the server
        
        Args:
            file_path (str): Path to file to upload
        
        Returns:
            bool: True if upload successful, False otherwise
        """
        try:
            # Check if already uploaded
            if file_path in self.uploaded_files:
                print(f"⏭️  Already uploaded: {os.path.basename(file_path)}")
                return True
            
            # Check if file exists and is accessible
            if not os.path.exists(file_path):
                print(f"❌ File not found: {file_path}")
                return False
            
            # Wait a bit to ensure file is fully written
            time.sleep(1)
            
            print(f"📤 Uploading: {os.path.basename(file_path)}")
            
            # Prepare request
            headers = {}
            if self.auth_token:
                headers['Authorization'] = f'Bearer {self.auth_token}'
            
            # Open and upload file
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f)}
                response = requests.post(
                    f'{self.server_url}/upload',
                    files=files,
                    headers=headers,
                    timeout=300  # 5 minutes timeout for large files
                )
            
            if response.status_code in [200, 201]:
                result = response.json()
                if result.get('duplicate'):
                    print(f"✅ File already exists on server (duplicate): {os.path.basename(file_path)}")
                else:
                    print(f"✅ Upload successful: {os.path.basename(file_path)}")
                
                # Mark as uploaded
                self.uploaded_files.add(file_path)
                self.save_uploaded_log(file_path)
                
                # Remove from failed list if it was there
                if file_path in self.failed_files:
                    del self.failed_files[file_path]
                
                return True
            else:
                print(f"❌ Upload failed: {response.status_code} - {response.text}")
                return False
        
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection error: Cannot reach server at {self.server_url}")
            return False
        except Exception as e:
            print(f"❌ Upload error: {str(e)}")
            return False
    
    def retry_failed_uploads(self):
        """Retry previously failed uploads"""
        if not self.failed_files:
            return
        
        print(f"\n🔄 Retrying {len(self.failed_files)} failed uploads...")
        
        failed_files_copy = dict(self.failed_files)
        for file_path, attempts in failed_files_copy.items():
            if attempts < config.RETRY_ATTEMPTS:
                if self.upload_file(file_path):
                    if file_path in self.failed_files:
                        del self.failed_files[file_path]
                else:
                    self.failed_files[file_path] = attempts + 1
            else:
                print(f"⚠️  Max retry attempts reached for: {os.path.basename(file_path)}")


class FileWatchHandler(FileSystemEventHandler):
    """Handle file system events"""
    
    def __init__(self, uploader, file_extensions):
        self.uploader = uploader
        self.file_extensions = file_extensions
    
    def on_created(self, event):
        """Called when a file is created"""
        if event.is_directory:
            return
        
        file_path = event.src_path
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # Check if file type should be uploaded
        if file_ext in self.file_extensions:
            print(f"\n🆕 New file detected: {os.path.basename(file_path)}")
            
            # Upload file
            if not self.uploader.upload_file(file_path):
                # Add to failed files for retry
                self.uploader.failed_files[file_path] = 1
    
    def on_modified(self, event):
        """Called when a file is modified"""
        # Some systems trigger modified instead of created
        if event.is_directory:
            return
        
        file_path = event.src_path
        
        # Only process if not already uploaded
        if file_path not in self.uploader.uploaded_files:
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext in self.file_extensions:
                time.sleep(1)  # Wait for file to be fully written
                if not self.uploader.upload_file(file_path):
                    self.uploader.failed_files[file_path] = 1


def scan_existing_files(watch_folder, uploader, file_extensions):
    """Scan for existing files in the watch folder and upload them"""
    print(f"\n🔍 Scanning existing files in: {watch_folder}")
    
    files_found = []
    for root, dirs, files in os.walk(watch_folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext in file_extensions:
                files_found.append(file_path)
    
    print(f"📁 Found {len(files_found)} files to check")
    
    # Upload files that haven't been uploaded yet
    new_uploads = 0
    for file_path in files_found:
        if file_path not in uploader.uploaded_files:
            if uploader.upload_file(file_path):
                new_uploads += 1
            else:
                uploader.failed_files[file_path] = 1
    
    print(f"✨ Uploaded {new_uploads} new files")


def main():
    """Main function"""
    print("=" * 60)
    print("Personal Cloud Storage - Auto Uploader")
    print("=" * 60)
    print(f"Server: {config.SERVER_URL}")
    print(f"Watch folder: {config.WATCH_FOLDER}")
    print(f"File types: {', '.join(config.FILE_EXTENSIONS)}")
    print("=" * 60)
    
    # Test server connection
    try:
        response = requests.get(config.SERVER_URL, timeout=5)
        print("✅ Server is reachable")
    except:
        print("⚠️  Warning: Cannot reach server. Will retry when uploading files.")
    
    # Create uploader
    uploader = FileUploader(
        config.SERVER_URL,
        config.AUTH_TOKEN if config.AUTH_TOKEN != 'your-secret-token-here' else None
    )
    
    # Scan for existing files
    scan_existing_files(config.WATCH_FOLDER, uploader, config.FILE_EXTENSIONS)
    
    # Set up file watcher
    event_handler = FileWatchHandler(uploader, config.FILE_EXTENSIONS)
    observer = Observer()
    observer.schedule(event_handler, config.WATCH_FOLDER, recursive=True)
    observer.start()
    
    print(f"\n👁️  Watching for new files... (Press Ctrl+C to stop)")
    
    try:
        retry_counter = 0
        while True:
            time.sleep(config.CHECK_INTERVAL)
            
            # Retry failed uploads every minute
            retry_counter += config.CHECK_INTERVAL
            if retry_counter >= 60:
                uploader.retry_failed_uploads()
                retry_counter = 0
    
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping uploader...")
        observer.stop()
    
    observer.join()
    print("👋 Goodbye!")


if __name__ == '__main__':
    main()
