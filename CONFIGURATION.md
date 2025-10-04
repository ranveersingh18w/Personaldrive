# Example Configuration Files

## Backend Configuration Options

### Minimum Configuration
```python
# backend/config.py
STORAGE_PATH = r'D:\MyCloud\Photos'
```

### Production Configuration
```python
# backend/config.py
import os

# Server settings
HOST = '0.0.0.0'
PORT = 5000
DEBUG = False  # Disable debug in production

# Storage settings
STORAGE_PATH = r'E:\Backups\PersonalCloud'
THUMBNAILS_PATH = os.path.join(STORAGE_PATH, '.thumbnails')
DATABASE_PATH = r'E:\Backups\PersonalCloud\storage.db'

# Upload settings
MAX_FILE_SIZE = 1000 * 1024 * 1024  # 1 GB
ALLOWED_EXTENSIONS = {
    'jpg', 'jpeg', 'png', 'gif', 'webp',
    'mp4', 'mov', 'avi'
}

# Security
REQUIRE_AUTH = True
AUTH_TOKEN = 'change-this-to-a-random-long-string'

os.makedirs(STORAGE_PATH, exist_ok=True)
os.makedirs(THUMBNAILS_PATH, exist_ok=True)
```

### Network Storage Configuration
```python
# backend/config.py
# For NAS or network drive
STORAGE_PATH = r'\\192.168.1.100\SharedFolder\Photos'

# Or mapped drive
STORAGE_PATH = r'Z:\Photos'
```

---

## Client Configuration Options

### Local Network Configuration
```python
# client/config.py
SERVER_URL = 'http://192.168.1.100:5000'
AUTH_TOKEN = 'match-your-backend-token'

WATCH_FOLDER = r'C:\Users\YourName\Pictures\Camera'
FILE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.mp4'}

CHECK_INTERVAL = 5
RETRY_ATTEMPTS = 3
```

### Multiple Watch Folders
Create separate config files and run multiple clients:

```python
# client/config_photos.py
SERVER_URL = 'http://localhost:5000'
WATCH_FOLDER = r'C:\Users\YourName\Pictures'
FILE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}
```

```python
# client/config_videos.py
SERVER_URL = 'http://localhost:5000'
WATCH_FOLDER = r'C:\Users\YourName\Videos'
FILE_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv'}
```

Run with:
```powershell
python uploader.py --config config_photos.py
python uploader.py --config config_videos.py
```

---

## Android (Termux) Configuration

### Basic Setup
```python
# client/config.py
SERVER_URL = 'http://192.168.1.100:5000'
AUTH_TOKEN = 'your-token'

# Android camera folder
WATCH_FOLDER = '/storage/emulated/0/DCIM/Camera'

FILE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.mp4'}
CHECK_INTERVAL = 10  # Check less frequently on mobile
```

### Save Battery
```python
# client/config.py
CHECK_INTERVAL = 30  # Check every 30 seconds instead of 5
RETRY_ATTEMPTS = 2  # Fewer retries
```

---

## Frontend Configuration

### Custom Backend URL
```json
// frontend/package.json
{
  "proxy": "http://192.168.1.100:5000"
}
```

Or edit `frontend/src/App.js`:
```javascript
const API_URL = 'http://192.168.1.100:5000';
```

---

## Windows Task Scheduler (Auto-Start)

### Auto-start Backend on Boot

1. Open Task Scheduler
2. Create Basic Task
3. Name: "Cloud Storage Backend"
4. Trigger: "When the computer starts"
5. Action: "Start a program"
6. Program: `C:\Users\YourName\Desktop\drive\start-backend.bat`

### Auto-start Client on Login

Same steps but:
- Trigger: "When I log on"
- Program: `C:\Users\YourName\Desktop\drive\start-client.bat`

---

## Firewall Rules

### Windows Firewall
Allow Python to accept connections:

```powershell
# Run as Administrator
netsh advfirewall firewall add rule name="Cloud Storage Server" dir=in action=allow program="C:\Python39\python.exe" enable=yes

# Or allow specific port
netsh advfirewall firewall add rule name="Cloud Storage Port" dir=in action=allow protocol=TCP localport=5000
```

---

## NGINX Reverse Proxy (Optional)

If you want to use HTTPS and a custom domain:

```nginx
# /etc/nginx/sites-available/cloud-storage
server {
    listen 443 ssl;
    server_name mycloud.local;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api/ {
        proxy_pass http://localhost:5000/;
        client_max_body_size 1G;
    }
}
```

---

## Docker Configuration (Advanced)

### Backend Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

EXPOSE 5000
CMD ["python", "app.py"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./storage:/app/storage
      - ./data:/app/data
    environment:
      - STORAGE_PATH=/app/storage
      - DATABASE_PATH=/app/data/storage.db
```

---

## Environment Variables

Instead of editing config.py, use environment variables:

```python
# backend/config.py
import os

STORAGE_PATH = os.getenv('STORAGE_PATH', default_fallback)
AUTH_TOKEN = os.getenv('AUTH_TOKEN', 'default-token')
```

Then set in PowerShell:
```powershell
$env:STORAGE_PATH = "D:\MyCloud"
$env:AUTH_TOKEN = "my-secret-token"
python app.py
```
