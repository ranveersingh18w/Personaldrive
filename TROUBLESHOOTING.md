# 🔧 Troubleshooting Guide

## Common Issues and Solutions

---

## 1. Installation Issues

### "pip is not recognized"

**Problem:** Python or pip not in PATH

**Solution:**
```powershell
# Option 1: Use python -m pip
python -m pip install -r requirements.txt

# Option 2: Reinstall Python with "Add to PATH" checked
# Download from https://www.python.org/
```

### "node is not recognized"

**Problem:** Node.js not installed or not in PATH

**Solution:**
1. Download from https://nodejs.org/
2. Install with default settings
3. Restart your terminal
4. Test: `node --version`

### "Permission denied" during installation

**Solution:**
```powershell
# Run as administrator
# Right-click PowerShell → Run as Administrator
```

---

## 2. Backend Server Issues

### Server won't start

**Error:** `Address already in use`

**Solution:**
```powershell
# Find what's using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or change port in backend/config.py
PORT = 8080
```

### "Cannot create storage folder"

**Solution:**
```python
# Edit backend/config.py with a valid path
STORAGE_PATH = r'C:\Users\YourName\Documents\MyCloud'

# Make sure you have write permissions
```

### "Module not found: PIL"

**Solution:**
```powershell
pip install Pillow
# Note: Package is called "Pillow" not "PIL"
```

### Database errors

**Solution:**
```powershell
# Delete and recreate database
cd backend
del storage.db
python app.py
# Database will be recreated automatically
```

---

## 3. Client Upload Issues

### "Cannot reach server"

**Problem:** Server not running or wrong URL

**Solution:**
```python
# 1. Check if server is running
# Open browser: http://localhost:5000

# 2. Check client/config.py
SERVER_URL = 'http://localhost:5000'  # For local
SERVER_URL = 'http://192.168.1.100:5000'  # For network

# 3. Check firewall
# Windows Firewall → Allow Python through
```

### "Files not uploading automatically"

**Problem:** Watch folder doesn't exist or is empty

**Solution:**
```python
# 1. Check watch folder exists
# Edit client/config.py
WATCH_FOLDER = r'C:\Users\YourName\Pictures'

# 2. Add a test photo to the folder

# 3. Check file extensions match
FILE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.mp4'}

# 4. Check client console for errors
```

### "Upload fails with 401 Unauthorized"

**Problem:** Authentication token mismatch

**Solution:**
```python
# Make sure tokens match in both files:

# backend/config.py
AUTH_TOKEN = 'my-secret-token'

# client/config.py
AUTH_TOKEN = 'my-secret-token'  # Must be the same!
```

### Client crashes or freezes

**Solution:**
```powershell
# 1. Check for errors in console output

# 2. Reduce check frequency
# Edit client/config.py
CHECK_INTERVAL = 10  # Instead of 5

# 3. Check disk space

# 4. Reinstall watchdog
pip install --upgrade watchdog
```

---

## 4. Frontend Issues

### "npm install fails"

**Solution:**
```powershell
# 1. Clear npm cache
npm cache clean --force

# 2. Delete node_modules and package-lock.json
cd frontend
rmdir /s node_modules
del package-lock.json

# 3. Reinstall
npm install

# 4. If still fails, try:
npm install --legacy-peer-deps
```

### Frontend won't start

**Error:** `Port 3000 already in use`

**Solution:**
```powershell
# Option 1: Kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F

# Option 2: Use different port
set PORT=3001
npm start
```

### "Failed to load files" in browser

**Problem:** Cannot connect to backend

**Solution:**
```javascript
// 1. Check backend is running
// Visit http://localhost:5000 in browser

// 2. Check browser console (F12) for CORS errors

// 3. Verify API_URL in frontend/src/App.js
const API_URL = 'http://localhost:5000';

// 4. Check proxy in frontend/package.json
"proxy": "http://localhost:5000"
```

### Images won't display

**Problem:** Thumbnail generation failed

**Solution:**
```powershell
# 1. Check backend logs for errors

# 2. Reinstall Pillow
pip install --upgrade Pillow

# 3. Check image file isn't corrupted

# 4. Try reuploading the image
```

---

## 5. Network Access Issues

### Can't access from phone

**Problem:** Firewall or wrong IP address

**Solution:**
```powershell
# 1. Find your PC's IP
ipconfig
# Look for IPv4 Address: 192.168.1.xxx

# 2. Allow through firewall
# Windows Firewall → Advanced → Inbound Rules
# New Rule → Port → TCP → 5000, 3000

# 3. Test on PC first
# Visit http://YOUR_PC_IP:3000 in PC browser

# 4. Make sure phone is on same WiFi network
```

### "Connection refused" from network

**Solution:**
```python
# backend/config.py
HOST = '0.0.0.0'  # Not 'localhost' or '127.0.0.1'
```

---

## 6. Upload/Download Issues

### Large files fail to upload

**Solution:**
```python
# Increase max file size in backend/config.py
MAX_FILE_SIZE = 2000 * 1024 * 1024  # 2 GB

# Also increase timeout in client/uploader.py
timeout=600  # 10 minutes
```

### Upload succeeds but file is corrupted

**Solution:**
```python
# Check disk space
# Check for write permissions
# Try uploading smaller test file first
```

### Downloads are slow

**Solution:**
```powershell
# 1. Use wired Ethernet instead of WiFi
# 2. Check disk speed (SSD vs HDD)
# 3. Close other applications using network
```

---

## 7. Database Issues

### "Database is locked"

**Solution:**
```powershell
# 1. Close all running instances
# 2. Delete database and restart
cd backend
del storage.db
python app.py
```

### "Files disappeared from web UI"

**Solution:**
```powershell
# Check if database file exists
dir backend\storage.db

# Check if physical files exist
dir %USERPROFILE%\MyCloud\Photos

# If database is missing but files exist:
# Backend will recreate DB but you'll need to re-upload metadata
```

---

## 8. Performance Issues

### Server is slow

**Solution:**
```python
# 1. Disable debug mode
# backend/config.py
DEBUG = False

# 2. Use faster storage (SSD)

# 3. Limit thumbnail generation
# Only generate for images under certain size

# 4. Add caching for thumbnails
```

### High CPU usage

**Solution:**
```python
# Increase check interval in client
# client/config.py
CHECK_INTERVAL = 30  # Check every 30 seconds

# Reduce thumbnail size
# backend/app.py
size=(200, 200)  # Instead of (300, 300)
```

### High memory usage

**Solution:**
```python
# Process files in batches
# Don't load all thumbnails at once
# Restart services periodically
```

---

## 9. Android/Termux Issues

### "Permission denied" on Android

**Solution:**
```bash
# Grant storage permissions
termux-setup-storage

# If that doesn't work, reinstall Termux from F-Droid
```

### "Cannot find camera folder"

**Solution:**
```python
# Try these paths in client/config.py:
WATCH_FOLDER = '/storage/emulated/0/DCIM/Camera'
WATCH_FOLDER = '/storage/emulated/0/DCIM'
WATCH_FOLDER = '/sdcard/DCIM/Camera'

# List folders to find correct path:
ls -la /storage/emulated/0/DCIM/
```

### Battery drain on phone

**Solution:**
```python
# Increase check interval
CHECK_INTERVAL = 60  # Check every minute

# Or run manually instead of automatically
```

---

## 10. Windows-Specific Issues

### "Execution policy" error in PowerShell

**Error:** `script.ps1 cannot be loaded because running scripts is disabled`

**Solution:**
```powershell
# Run as Administrator:
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or use .bat files instead of .ps1
```

### "Python was not found"

**Solution:**
```powershell
# 1. Check if Python is installed
python --version

# 2. If not found, try:
py --version

# 3. Add Python to PATH manually:
# System Properties → Environment Variables → Path
# Add: C:\Python39 and C:\Python39\Scripts
```

### Batch files don't work

**Solution:**
```powershell
# 1. Right-click → Edit to see the error
# 2. Run commands manually one by one
# 3. Check file paths are correct
```

---

## 11. Testing & Debugging

### Run diagnostic test

```powershell
python test-setup.py
```

### Check if server is accessible

```powershell
# Test from command line
curl http://localhost:5000

# Or in PowerShell
Invoke-WebRequest http://localhost:5000
```

### View detailed logs

```python
# Add logging to backend/app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test file upload manually

```powershell
# Using curl
curl -X POST http://localhost:5000/upload -F "file=@test.jpg"

# Using Python
python
>>> import requests
>>> with open('test.jpg', 'rb') as f:
...     requests.post('http://localhost:5000/upload', files={'file': f})
```

---

## 12. Getting Help

### Before asking for help:

1. ✅ Run `python test-setup.py`
2. ✅ Check all services are running
3. ✅ Look at console output for errors
4. ✅ Try with a small test file first
5. ✅ Check this troubleshooting guide

### Information to provide:

- Operating system and version
- Python version (`python --version`)
- Node.js version (`node --version`)
- Exact error message
- What you were trying to do
- Console output from all services

---

## 13. Clean Reinstall

If nothing works, try a clean reinstall:

```powershell
# 1. Stop all services (Ctrl+C in all terminals)

# 2. Delete generated files
cd backend
del storage.db
rmdir /s MyCloud

cd ../client
del uploaded_files.log

cd ../frontend
rmdir /s node_modules
del package-lock.json

# 3. Reinstall everything
cd ..
python -m pip install --upgrade pip
python setup.bat

# 4. Start fresh
python start-all.bat
```

---

## 14. Emergency Recovery

### Lost database but files still exist

```python
# Files are safe in storage folder!
# Just restart server - it will create new DB
# You'll need to re-upload metadata by copying files back to watch folder
```

### Accidentally deleted files

```powershell
# Check Windows Recycle Bin
# If enabled backup, restore from backup location
# Files are in: %USERPROFILE%\MyCloud\Photos
```

---

## 15. Preventive Measures

### Regular backups

```powershell
# Backup entire storage folder
xcopy /E /I "%USERPROFILE%\MyCloud\Photos" "D:\Backup\Photos"

# Backup database
copy backend\storage.db backend\storage.db.backup
```

### Monitor disk space

```powershell
# Check free space
wmic logicaldisk get caption,freespace,size

# Set up alerts when low on space
```

### Keep logs

```python
# Enable logging in backend/app.py
import logging
logging.basicConfig(
    filename='server.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)
```

---

## Still Having Issues?

1. Check GitHub Issues (if project is on GitHub)
2. Review all documentation files
3. Try on a different computer to isolate the issue
4. Test with minimal configuration first
5. Check for Windows updates that might have broken something

**Remember:** Most issues are configuration-related. Double-check all config files!

---

**Pro Tip:** Keep a backup of your working configuration files so you can always revert to a known-good state!
