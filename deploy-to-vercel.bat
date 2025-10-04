@echo off
echo ========================================
echo GitHub and Vercel Deployment Guide
echo ========================================
echo.
echo Your git repository is ready!
echo.
echo STEP 1: Create GitHub Repository
echo --------------------------------
echo 1. Go to https://github.com/new
echo 2. Repository name: personal-cloud-storage
echo 3. Make it PUBLIC or PRIVATE
echo 4. DO NOT initialize with README
echo 5. Click "Create repository"
echo.
echo STEP 2: Push to GitHub
echo ----------------------
echo Copy your repository URL (it looks like):
echo   https://github.com/YOUR_USERNAME/personal-cloud-storage.git
echo.
set /p REPO_URL="Paste your GitHub repository URL here: "
echo.
echo Pushing to GitHub...
git remote add origin %REPO_URL%
git push -u origin main
echo.
if errorlevel 1 (
    echo ERROR: Failed to push to GitHub
    echo Make sure you have git credentials configured
    pause
    exit /b 1
)
echo.
echo ✅ Successfully pushed to GitHub!
echo.
echo ========================================
echo.
echo STEP 3: Deploy Frontend to Vercel
echo ----------------------------------
echo.
echo Installing Vercel CLI...
call npm install -g vercel
echo.
echo Now deploying to Vercel...
cd frontend
call vercel --prod
cd ..
echo.
echo ========================================
echo.
echo ✅ DEPLOYMENT COMPLETE!
echo.
echo Next Steps:
echo 1. Your frontend is now live on Vercel
echo 2. Start your backend: cd backend && python app.py
echo 3. Start ngrok: ngrok http 5000
echo 4. Copy your ngrok URL
echo 5. Go to Vercel Dashboard → Settings → Environment Variables
echo 6. Add: REACT_APP_API_URL = YOUR_NGROK_URL
echo 7. Redeploy: vercel --prod
echo.
echo ========================================
pause
# backend/config.py
REQUIRE_AUTH = True
AUTH_TOKEN = "your-secret-key-change-this"
