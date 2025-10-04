#!/bin/bash
# Deployment script for Personal Cloud Storage

echo "========================================"
echo "Personal Cloud Storage - Deployment"
echo "========================================"
echo ""

# Step 1: GitHub
echo "Step 1: Create GitHub Repository"
echo "--------------------------------"
echo "Go to: https://github.com/new"
echo "Repository name: personal-cloud-storage"
echo ""
read -p "Enter your GitHub repository URL: " REPO_URL
echo ""

echo "Pushing to GitHub..."
git remote add origin "$REPO_URL"
git push -u origin main

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to push to GitHub"
    exit 1
fi

echo ""
echo "✅ Successfully pushed to GitHub!"
echo ""

# Step 2: Vercel
echo "Step 2: Deploy to Vercel"
echo "------------------------"
echo "Installing Vercel CLI..."
npm install -g vercel

echo ""
echo "Deploying frontend to Vercel..."
cd frontend
vercel --prod
cd ..

echo ""
echo "========================================"
echo "✅ DEPLOYMENT COMPLETE!"
echo "========================================"
echo ""
echo "Next Steps:"
echo "1. Start backend: cd backend && python app.py"
echo "2. Start ngrok: ngrok http 5000"
echo "3. Add REACT_APP_API_URL to Vercel (Settings → Environment Variables)"
echo "4. Redeploy: vercel --prod"
echo ""
