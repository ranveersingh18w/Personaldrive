# Personal Cloud Storage

A self-hosted cloud storage solution for automatically backing up photos and videos.

## 🚀 Features

- **Automatic Backup**: Client app monitors folders and auto-uploads new photos/videos
- **Local Storage**: Files stored safely on your Windows PC or external drive
- **Web Interface**: View, download, and manage your files through a browser
- **Cross-Platform Client**: Python-based client works on Windows, macOS, Linux, and Android (via Termux)
- **Secure**: Optional authentication and encryption support

## 📁 Project Structure

```
drive/
├── backend/           # Flask server
│   ├── app.py        # Main server application
│   ├── database.py   # SQLite database handlers
│   ├── config.py     # Configuration settings
│   └── requirements.txt
├── client/           # Upload client
│   ├── uploader.py   # Main client script with auto-watch
│   ├── config.py     # Client configuration
│   └── requirements.txt
└── frontend/         # React web UI
    ├── public/
    └── src/
```

## 🛠️ Setup Instructions

### Backend (Server)

1. Navigate to backend folder:
```powershell
cd backend
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
```

3. Configure storage location in `config.py`

4. Run the server:
```powershell
python app.py
```

Server will start at `http://localhost:5000`

### Client (Uploader)

1. Navigate to client folder:
```powershell
cd client
```

2. Install dependencies:
```powershell
pip install -r requirements.txt
```

3. Configure settings in `config.py`:
   - Set your server URL
   - Set folder to watch for new files

4. Run the client:
```powershell
python uploader.py
```

### Frontend (Web UI)

1. Navigate to frontend folder:
```powershell
cd frontend
```

2. Install dependencies:
```powershell
npm install
```

3. Start development server:
```powershell
npm start
```

Web UI will open at `http://localhost:3000`

## 📝 Usage

### Automatic Upload
- Place photos/videos in the watched folder
- Client automatically detects and uploads them
- Check web interface to view uploaded files

### Manual Upload
- Use web interface to upload files manually
- Drag and drop supported

### Manage Files
- View thumbnails in web interface
- Download or delete files
- Search and filter by date/type

## ⚙️ Configuration

### Backend Settings (`backend/config.py`)
- `STORAGE_PATH`: Where files are stored (e.g., `D:\MyCloud\Photos`)
- `DATABASE_PATH`: SQLite database location
- `PORT`: Server port (default: 5000)
- `MAX_FILE_SIZE`: Maximum upload size

### Client Settings (`client/config.py`)
- `SERVER_URL`: Backend server address
- `WATCH_FOLDER`: Folder to monitor for new files
- `FILE_TYPES`: File extensions to upload

## 🔒 Security Features (Optional)

- Add authentication tokens
- Enable HTTPS
- Encrypt files before storage
- Set up firewall rules to limit access to local network

## 🎯 Future Enhancements

- [ ] User authentication system
- [ ] File encryption
- [ ] Video thumbnail generation
- [ ] Auto-compression for large files
- [ ] Backup to external HDD
- [ ] Mobile app (Flutter/React Native)
- [ ] Face recognition and tagging
- [ ] Photo gallery view like Google Photos

## 📱 Mobile Setup (Android via Termux)

1. Install Termux from F-Droid
2. Install Python: `pkg install python`
3. Copy client folder to Android
4. Run: `python uploader.py`

## 🤝 Contributing

Feel free to add features and improvements!

## 📄 License

MIT License - Free to use and modify
