# Quick Start - Personal Cloud Storage

## 🚀 Getting Started in 3 Steps

### Step 1: Start the Backend Server

```powershell
cd backend
pip install -r requirements.txt
python app.py
```

The server will start at `http://localhost:5000`

**Important:** By default, files are stored in `C:\Users\YourUsername\MyCloud\Photos`. You can change this in `backend\config.py`.

### Step 2: Start the Client Uploader (Optional)

In a new terminal:

```powershell
cd client
pip install -r requirements.txt
python uploader.py
```

The client will monitor your Camera Roll folder and automatically upload new photos/videos. Configure the watch folder in `client\config.py`.

### Step 3: Start the Web Interface

In another terminal:

```powershell
cd frontend
npm install
npm start
```

The web interface will open at `http://localhost:3000`

---

## 📱 Access from Your Phone

### Option 1: Use the Web Interface

1. Find your PC's IP address:
```powershell
ipconfig
```
Look for "IPv4 Address" (e.g., 192.168.1.100)

2. On your phone's browser, visit:
```
http://YOUR_PC_IP:3000
```

3. Upload photos directly from your phone!

### Option 2: Run Python Client on Android (via Termux)

1. Install [Termux](https://f-droid.org/en/packages/com.termux/) from F-Droid

2. In Termux, run:
```bash
pkg install python git
pip install watchdog requests
```

3. Copy the `client` folder to your Android device

4. Edit `config.py` to set your PC's IP address:
```python
SERVER_URL = 'http://192.168.1.100:5000'
WATCH_FOLDER = '/storage/emulated/0/DCIM/Camera'
```

5. Grant storage permissions:
```bash
termux-setup-storage
```

6. Run the client:
```bash
python uploader.py
```

Now your phone will automatically upload new photos!

---

## 🔧 Configuration Tips

### Change Storage Location

Edit `backend\config.py`:

```python
# Store on external drive
STORAGE_PATH = r'D:\MyCloud\Photos'

# Or on a network drive
STORAGE_PATH = r'\\NAS\Backups\Photos'
```

### Enable Authentication

Edit `backend\config.py`:

```python
REQUIRE_AUTH = True
AUTH_TOKEN = 'your-super-secret-token-here'
```

Then update `client\config.py` with the same token:

```python
AUTH_TOKEN = 'your-super-secret-token-here'
```

### Change Port

If port 5000 is already in use, edit `backend\config.py`:

```python
PORT = 8080  # Or any other port
```

Then update the frontend and client to use the new port.

---

## 🛡️ Network Security

### For Local Network Only (Recommended)

Your setup is already configured for local network access. The server listens on `0.0.0.0` which means it's accessible from other devices on your network.

### To Allow Internet Access

1. Set up port forwarding on your router (forward port 5000)
2. Use a dynamic DNS service to get a permanent domain
3. **Strongly recommended:** Enable authentication and use HTTPS
4. Consider using a VPN instead for secure remote access

---

## 📊 Monitoring

### View Server Logs

The server prints all activity to the console. Watch for:
- ✅ Successful uploads
- ❌ Errors
- 📊 File statistics

### Check Storage Usage

Visit `http://localhost:5000/stats` to see:
- Total files
- Total size
- Images vs videos count

---

## 🔥 Troubleshooting

### "Cannot reach server"

1. Check if the server is running:
```powershell
netstat -an | findstr :5000
```

2. Check your firewall settings - allow Python through

3. Try accessing `http://localhost:5000` in your browser

### "Upload failed"

1. Check file permissions on storage folder
2. Verify disk space available
3. Check if file type is allowed (see `config.py`)

### "Client not uploading"

1. Verify watch folder exists
2. Check server URL in `client\config.py`
3. Look for errors in client console
4. Try manually adding a photo to the watch folder

---

## 🎯 What's Next?

### Phase 1 (Current)
- ✅ Basic upload/download
- ✅ Web interface
- ✅ Auto-sync client
- ✅ Thumbnail generation

### Phase 2 (Future Enhancements)
- [ ] Video thumbnails
- [ ] User authentication UI
- [ ] File encryption
- [ ] Duplicate detection
- [ ] Compression options
- [ ] Backup to cloud (Google Drive, OneDrive)
- [ ] Face recognition
- [ ] Mobile app (React Native/Flutter)

---

## 💡 Tips

- **Backup regularly:** Set up Windows Task Scheduler to backup your storage folder
- **External HDD:** Point storage to an external drive for safety
- **Network speed:** Use wired Ethernet for faster uploads
- **Mobile data:** Client only uploads when connected to Wi-Fi by default
- **Organize:** Create subfolders in storage location for better organization

---

## 🆘 Need Help?

Check the main `README.md` for detailed documentation, or:

1. Check server logs for errors
2. Verify all services are running
3. Test with small files first
4. Make sure firewall allows connections

Enjoy your personal cloud storage! 🎉
