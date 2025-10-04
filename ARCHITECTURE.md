# 🏗️ System Architecture

## Overview Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     PERSONAL CLOUD STORAGE                       │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│   Upload Client  │         │  Backend Server  │         │  Web Interface   │
│   (Python)       │────────▶│  (Flask/Python)  │◀────────│  (React)         │
│                  │  HTTP   │                  │  HTTP   │                  │
│  - Watchdog      │  POST   │  - REST API      │  GET    │  - File Grid     │
│  - Auto-upload   │  /upload│  - SQLite DB     │  POST   │  - Upload UI     │
│  - Retry logic   │         │  - Thumbnails    │  DELETE │  - Search        │
└──────────────────┘         │  - File Storage  │         │  - Stats         │
                             └──────────────────┘         └──────────────────┘
                                      │                             │
                                      ▼                             ▼
                             ┌──────────────────┐         ┌──────────────────┐
                             │   File System    │         │     Browser      │
                             │                  │         │                  │
                             │  📁 Photos/      │         │  localhost:3000  │
                             │  📁 Thumbnails/  │         │  192.168.x.x:3000│
                             │  🗄️ SQLite DB    │         └──────────────────┘
                             └──────────────────┘
```

---

## Component Details

### 1. Upload Client (Auto-Uploader)

**Location:** `client/uploader.py`

**Purpose:** Monitors folders and automatically uploads new files

**Key Features:**
- 👁️ Watches specified folders for changes
- 📤 Automatically uploads new photos/videos
- 🔄 Retries failed uploads
- 📝 Tracks uploaded files to prevent duplicates
- ⚡ Works 24/7 in background

**Dependencies:**
- `watchdog` - File system monitoring
- `requests` - HTTP client for API calls

**Configuration:** `client/config.py`

**Flow:**
```
Watch Folder → Detect New File → Upload to Server → Log Success
     ↓              ↓                    ↓               ↓
  Camera Roll   File Created        HTTP POST        Save to Log
  Pictures      Event Triggered     /upload          (prevent re-upload)
```

---

### 2. Backend Server (API & Storage)

**Location:** `backend/app.py`

**Purpose:** Central server handling all storage operations

**Key Features:**
- 🌐 REST API for file operations
- 💾 SQLite database for metadata
- 🖼️ Automatic thumbnail generation
- 🔍 Search and filter capabilities
- 📊 Storage statistics
- 🔒 Optional authentication

**Dependencies:**
- `Flask` - Web framework
- `Flask-CORS` - Cross-origin requests
- `Pillow` - Image processing
- `Werkzeug` - File handling

**Configuration:** `backend/config.py`

**Database Schema:**
```sql
Files Table:
- id (PRIMARY KEY)
- filename
- original_filename
- file_path
- file_size
- file_type (image/video)
- mime_type
- upload_date
- created_date
- thumbnail_path
- width, height
- duration
- checksum (MD5)
```

**API Endpoints:**
```
POST   /upload          → Upload new file
GET    /files           → List all files (with filters)
GET    /file/<id>       → Download specific file
GET    /thumbnail/<id>  → Get thumbnail image
DELETE /file/<id>       → Delete file
GET    /stats           → Storage statistics
GET    /search?q=...    → Search files
```

---

### 3. Web Interface (Frontend)

**Location:** `frontend/src/`

**Purpose:** User-friendly web interface for managing files

**Key Features:**
- 📤 Drag & drop upload
- 🖼️ Grid view with thumbnails
- 🔍 Search functionality
- 🎯 Filter by type (images/videos)
- 📊 Statistics dashboard
- ⬇️ Download files
- 🗑️ Delete files
- 📱 Responsive design

**Dependencies:**
- `React` - UI framework
- `axios` - HTTP client
- `react-dropzone` - Drag & drop upload

**Configuration:** `frontend/package.json`

**Components:**
```
App.js
├── Stats.js           → Display storage statistics
├── FileUpload.js      → Drag & drop upload interface
├── SearchBar.js       → Search input
└── FileGrid.js        → Display files in grid
```

---

## Data Flow

### Upload Flow (Client)
```
1. File created in watch folder
   └─▶ Watchdog detects event
      └─▶ Client reads file
         └─▶ Calculate MD5 checksum
            └─▶ HTTP POST to /upload
               └─▶ Server receives file
                  └─▶ Check for duplicate (checksum)
                     └─▶ Save to disk
                        └─▶ Generate thumbnail (if image)
                           └─▶ Store metadata in DB
                              └─▶ Return file ID
                                 └─▶ Client logs success
```

### Upload Flow (Web)
```
1. User drops file in browser
   └─▶ React captures file
      └─▶ FormData created
         └─▶ axios POST to /upload
            └─▶ Progress callback updates UI
               └─▶ Server processes (same as above)
                  └─▶ Response updates file list
```

### Download Flow
```
1. User clicks download button
   └─▶ GET /file/<id>
      └─▶ Server queries database
         └─▶ Find file path
            └─▶ Send file with headers
               └─▶ Browser downloads file
```

### View Flow
```
1. User opens web interface
   └─▶ GET /files
      └─▶ Server queries database
         └─▶ Return file list with metadata
            └─▶ React renders grid
               └─▶ For each image:
                  └─▶ GET /thumbnail/<id>
                     └─▶ Server sends thumbnail
                        └─▶ Image displayed in grid
```

---

## Storage Structure

```
MyCloud/
├── Photos/
│   ├── 20250104_120000_photo1.jpg    ← Original files
│   ├── 20250104_120530_photo2.jpg
│   ├── 20250104_121000_video1.mp4
│   └── ...
│
└── .thumbnails/
    ├── thumb_20250104_120000_photo1.jpg  ← Generated thumbnails
    ├── thumb_20250104_120530_photo2.jpg
    └── ...

backend/
└── storage.db  ← SQLite database with metadata
```

---

## Network Architecture

### Local Network Setup
```
┌─────────────────────────────────────────────────────────────┐
│                      Home Network (WiFi/LAN)                 │
│                                                               │
│  ┌──────────────┐          ┌──────────────┐                │
│  │   Windows PC │          │  Phone/Tablet│                │
│  │              │          │              │                │
│  │  Backend     │◀────────▶│  Browser     │                │
│  │  :5000       │   HTTP   │  :3000       │                │
│  │              │          │              │                │
│  │  Frontend    │          │  Upload      │                │
│  │  :3000       │          │  View        │                │
│  │              │          │  Download    │                │
│  └──────────────┘          └──────────────┘                │
│  192.168.1.100             192.168.1.50                     │
└─────────────────────────────────────────────────────────────┘
```

### Port Usage
```
5000  → Backend API Server
3000  → Frontend Web Server
```

---

## Security Model

### Current (Development)
```
┌──────────────┐
│    Client    │
└──────┬───────┘
       │ HTTP (unencrypted)
       ▼
┌──────────────┐
│   Backend    │
└──────┬───────┘
       │ Local filesystem
       ▼
┌──────────────┐
│  File System │
└──────────────┘
```

### Recommended (Production)
```
┌──────────────┐
│    Client    │
└──────┬───────┘
       │ HTTPS (encrypted)
       │ + Bearer Token
       ▼
┌──────────────┐
│   Backend    │ ← Firewall rules
└──────┬───────┘ ← Authentication
       │ Local/Network filesystem
       ▼
┌──────────────┐
│  File System │ ← Encrypted disk
└──────────────┘
```

---

## Scalability Options

### Current (Single PC)
```
All services on one machine
├── Backend
├── Frontend
└── Storage
```

### Future (Distributed)
```
Backend Server (PC 1)
├── API
└── Database
    │
    ├─▶ Storage Server (PC 2 / NAS)
    │   └── Files on large HDD/RAID
    │
    └─▶ Frontend (PC 1 or Cloud)
        └── Served via NGINX
```

### Cloud Hybrid
```
Local Storage (PC)
└─▶ Sync to Cloud
    ├── Google Drive
    ├── OneDrive
    └── Dropbox
```

---

## Monitoring Points

```
┌─────────────────┐
│  Application    │
│  Monitoring     │
└────────┬────────┘
         │
    ┌────┴────┬────────┬────────────┐
    ▼         ▼        ▼            ▼
┌───────┐ ┌──────┐ ┌──────┐ ┌──────────┐
│ Logs  │ │ Stats│ │ Disk │ │ Network  │
│       │ │      │ │Space │ │ Traffic  │
│ Flask │ │ /api │ │ Used │ │ Bandwidth│
│ logs  │ │/stats│ │      │ │          │
└───────┘ └──────┘ └──────┘ └──────────┘
```

**Key Metrics to Monitor:**
- Upload success/failure rate
- Storage space remaining
- Number of files
- Average upload time
- Server response time
- Network bandwidth usage

---

## Technology Stack

```
┌──────────────────────────────────────────────┐
│                  Frontend                     │
│  React + JavaScript + CSS                    │
│  react-dropzone, axios                       │
└──────────────┬───────────────────────────────┘
               │ HTTP/REST
┌──────────────▼───────────────────────────────┐
│                  Backend                      │
│  Python 3.7+ + Flask                         │
│  Flask-CORS, Pillow, Werkzeug               │
└──────────────┬───────────────────────────────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌──────────┐
│SQLite  │ │ File   │ │  Thumbnails│
│Database│ │ System │ │            │
└────────┘ └────────┘ └──────────┘
```

**Python Libraries:**
- Flask: Web framework
- SQLite3: Database
- Pillow: Image processing
- Watchdog: File monitoring
- Requests: HTTP client

**JavaScript Libraries:**
- React: UI framework
- Axios: HTTP client
- React Dropzone: File uploads

---

## Deployment Scenarios

### Scenario 1: Personal Use (Single PC)
```
Your PC
├── Backend (always running)
├── Frontend (when needed)
└── Client (always running)
```

### Scenario 2: Family/Multi-Device
```
Main PC (Server)
├── Backend (24/7)
└── Storage

Other Devices
├── Phone → Web Interface
├── Laptop → Web Interface + Client
└── Tablet → Web Interface
```

### Scenario 3: Remote Access
```
Home PC
├── Backend
├── Router (port forwarding)
└── Dynamic DNS

Remote Access
├── VPN → Secure access
└── HTTPS → Public access
```

---

## Development Workflow

```
1. Edit Code
   ├── Backend: backend/*.py
   ├── Client: client/*.py
   └── Frontend: frontend/src/*

2. Test Locally
   ├── Start backend: python app.py
   ├── Start client: python uploader.py
   └── Start frontend: npm start

3. Verify
   ├── Upload test file
   ├── Check web interface
   └── Review logs

4. Deploy
   ├── Stop services
   ├── Update code
   └── Restart services
```

---

## Backup Strategy

```
Primary Storage
└── c:\Users\...\MyCloud\Photos\
    │
    ├─▶ Local Backup (Automated)
    │   └── D:\Backups\Photos\
    │
    ├─▶ External HDD (Weekly)
    │   └── E:\Backups\Photos\
    │
    └─▶ Cloud Backup (Optional)
        └── Google Drive, OneDrive, etc.
```

---

This architecture provides:
- ✅ Flexibility (run components separately)
- ✅ Scalability (add more storage/users)
- ✅ Reliability (automatic retries)
- ✅ Performance (local storage, thumbnails)
- ✅ Security (optional auth, local network)
- ✅ Extensibility (easy to add features)
