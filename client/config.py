"""
Client Configuration
"""
import os

# Server settings
SERVER_URL = 'https://nonteachable-extravertive-allegra.ngrok-free.dev'  # Change to your server IP if remote

# Authentication (if enabled on server)
AUTH_TOKEN = 'your-secret-token-here'  # Must match server token

# Folder to watch for new files
WATCH_FOLDER = os.path.join(os.path.expanduser('~'), 'Pictures', 'Camera Roll')

# Alternatively, watch a specific folder:
# WATCH_FOLDER = r'D:\Photos\ToUpload'

# File types to upload (images and videos)
FILE_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp',  # Images
    '.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'  # Videos
}

# Upload settings
CHECK_INTERVAL = 5  # Seconds between checking for new files
RETRY_ATTEMPTS = 3  # Number of retry attempts for failed uploads
RETRY_DELAY = 10  # Seconds to wait before retrying

# Create watch folder if it doesn't exist
os.makedirs(WATCH_FOLDER, exist_ok=True)
