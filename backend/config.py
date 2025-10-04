"""
Backend Server Configuration
"""
import os

# Server settings
HOST = '0.0.0.0'  # Listen on all interfaces (accessible from network)
PORT = 5000
DEBUG = False  # Disabled for Python 3.13 compatibility

# Storage settings
STORAGE_PATH = os.path.join(os.path.expanduser('~'), 'MyCloud', 'Photos')
THUMBNAILS_PATH = os.path.join(STORAGE_PATH, '.thumbnails')
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'storage.db')

# Upload settings
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500 MB
ALLOWED_EXTENSIONS = {
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp',  # Images
    'mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv', 'webm'  # Videos
}

# Security settings (optional - set to enable authentication)
REQUIRE_AUTH = False
AUTH_TOKEN = 'your-secret-token-here'  # Change this!

# Create directories if they don't exist
os.makedirs(STORAGE_PATH, exist_ok=True)
os.makedirs(THUMBNAILS_PATH, exist_ok=True)
