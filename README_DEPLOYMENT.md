# 🚀 Deployment Guide

## Architecture

- **Frontend:** Vercel (React app)
- **Backend:** Your PC (Flask server + Storage)
- **Tunnel:** Ngrok (exposes your PC to internet)

---

## 📋 Deployment Steps

### 1. Setup GitHub Repository

```bash
cd C:\Users\Admin\Desktop\drive
git init
git add .
git commit -m "Initial commit - Personal Cloud Storage"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/personal-cloud-storage.git
git push -u origin main
```

### 2. Deploy Frontend to Vercel

```bash
cd frontend
npm install -g vercel
vercel login
vercel --prod
```

### 3. Setup Backend (Your PC)

**Terminal 1 - Run Backend:**
```bash
cd backend
python app.py
```

**Terminal 2 - Run Ngrok:**
```bash
ngrok http 5000
```

Copy the ngrok URL (e.g., `https://abc123.ngrok-free.app`)

### 4. Configure Vercel Environment Variable

Go to your Vercel dashboard:
1. Select your project
2. Settings → Environment Variables
3. Add:
   - **Name:** `REACT_APP_API_URL`
   - **Value:** `https://YOUR-NGROK-URL.ngrok-free.app`
4. Redeploy: `vercel --prod`

---

## 🔗 Access Your App

- **Frontend:** `https://your-app.vercel.app`
- **Backend:** Running on your PC
- **Storage:** Your PC's hard drive

---

## 🔐 Security Recommendations

1. Enable authentication in `backend/config.py`:
```python
REQUIRE_AUTH = True
AUTH_TOKEN = "your-secret-token"
```

2. Update frontend to send auth token

3. Use HTTPS only (ngrok provides this by default)

---

## 💡 Pro Tips

- **Ngrok Static Domain:** Upgrade to Pro ($8/month) for permanent URL
- **Auto-start Backend:** Use Windows Task Scheduler
- **Keep PC Running:** For 24/7 access
- **Monitor Logs:** Check backend terminal for activity

---

## 🆘 Troubleshooting

**Frontend can't reach backend:**
- Check ngrok is running
- Update REACT_APP_API_URL in Vercel
- Check backend CORS settings

**Uploads failing:**
- Check disk space on PC
- Verify backend is running
- Check firewall settings
