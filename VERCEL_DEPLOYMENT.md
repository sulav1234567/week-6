# Vercel Deployment Guide - Quiz Authoring Platform

This guide will help you deploy your Quiz Authoring Platform to Vercel for the frontend and provide options for the backend.

## 🎯 Overview

**What gets deployed where:**
- **Frontend (React + Vite)**: Vercel ✅
- **Backend (FastAPI)**: Render, Railway, or Vercel Serverless Functions

## 📋 Prerequisites

- GitHub account (you already have: `https://github.com/sulav1234567/week-6.git`)
- Vercel account (sign up at [vercel.com](https://vercel.com))
- Backend deployed somewhere (see Backend Options below)

## 🚀 Step 1: Deploy Frontend to Vercel

### Option A: Using Vercel Dashboard (Easiest)

1. **Go to Vercel**:
   - Visit [vercel.com](https://vercel.com)
   - Click "Sign Up" or "Login"
   - Choose "Continue with GitHub"

2. **Import Your Repository**:
   - Click "Add New Project"
   - Select "Import Git Repository"
   - Find and select: `sulav1234567/week-6`
   - Click "Import"

3. **Configure Build Settings**:
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```

4. **Environment Variables** (Add these):
   ```
   VITE_API_URL=https://your-backend-url.com
   ```

5. **Deploy**:
   - Click "Deploy"
   - Wait for deployment to complete (~2-3 minutes)
   - Your app will be live at: `https://your-project-name.vercel.app`

### Option B: Using Vercel CLI

```bash
# Install Vercel CLI globally
npm install -g vercel

# Navigate to your project
cd "/Users/sulavkhatiwada/Desktop/week 6/quiz-platform"

# Login to Vercel
vercel login

# Deploy
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (select your account)
# - Link to existing project? No
# - Project name? quiz-platform
# - In which directory is your code located? ./frontend
# - Want to override settings? Yes
#   - Build Command: npm run build
#   - Output Directory: dist
#   - Development Command: npm run dev

# For production deployment
vercel --prod
```

## 🔧 Step 2: Backend Deployment Options

Since Vercel is primarily for frontends, you have several options for the backend:

### Option 1: Render (Recommended - Free Tier Available)

1. **Create Render Account**:
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `sulav1234567/week-6`
   - Configure:
     ```
     Name: quiz-platform-backend
     Root Directory: backend
     Environment: Python 3
     Build Command: pip install -r requirements.txt
     Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

3. **Set Environment Variables**:
   ```
   PYTHON_VERSION=3.11
   ```

4. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment (~3-5 minutes)
   - Note your backend URL: `https://quiz-platform-backend.onrender.com`

5. **Update Frontend**:
   - Go back to Vercel dashboard
   - Update environment variable:
     ```
     VITE_API_URL=https://quiz-platform-backend.onrender.com
     ```
   - Redeploy frontend

### Option 2: Railway (Another Free Option)

1. **Create Railway Account**:
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy Backend**:
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `sulav1234567/week-6`
   - Railway will auto-detect Python
   - Add start command in settings:
     ```
     uvicorn main:app --host 0.0.0.0 --port $PORT
     ```

3. **Get Backend URL**:
   - Click "Settings" → "Domains"
   - Copy the generated URL

4. **Update Vercel**:
   - Update `VITE_API_URL` in Vercel with Railway backend URL

### Option 3: Vercel Serverless Functions (Advanced)

If you want everything on Vercel, you can convert your FastAPI backend to serverless functions:

1. **Install Vercel adapter**:
   ```bash
   cd backend
   pip install mangum
   ```

2. **Create `api/index.py`**:
   ```python
   from mangum import Mangum
   from main import app
   
   handler = Mangum(app)
   ```

3. **Update `vercel.json`** (already created for you):
   ```json
   {
     "rewrites": [
       { "source": "/api/(.*)", "destination": "/api/index" }
     ]
   }
   ```

**Note**: This option requires more setup and may have cold start issues.

## 🔄 Step 3: Update Frontend Configuration

### Update API URL in Frontend

You need to update your frontend to use the deployed backend URL instead of localhost.

**Option A: Using Environment Variables (Recommended)**

1. Create `.env.production` in `frontend/` directory:
   ```bash
   VITE_API_URL=https://your-backend-url.com
   ```

2. Update your API calls to use environment variable (if not already done).

**Option B: Direct Configuration**

Update API calls in your React components to use the production backend URL.

### Update CORS in Backend

Update `backend/main.py` to allow your Vercel domain:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://your-project-name.vercel.app",  # Add your Vercel URL
        "https://*.vercel.app",  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🎨 Step 4: Configure Custom Domain (Optional)

### On Vercel:

1. **Add Domain**:
   - Go to Project Settings → Domains
   - Add your custom domain
   - Follow DNS configuration instructions

2. **SSL Certificate**:
   - Automatically provisioned by Vercel

## 📊 Deployment Architecture

```
┌─────────────────────────────────────────┐
│           User's Browser                │
└──────────────┬──────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│     Vercel CDN (Frontend Hosting)        │
│  https://your-project.vercel.app         │
│  - React App                              │
│  - Static Assets                          │
└──────────────┬───────────────────────────┘
               │
               │ API Calls
               ▼
┌──────────────────────────────────────────┐
│   Backend (Render/Railway/Vercel)        │
│   https://your-backend.onrender.com      │
│   - FastAPI                               │
│   - SQLite/PostgreSQL                     │
└───────────────────────────────────────────┘
```

## ✅ Post-Deployment Checklist

- [ ] Frontend deployed to Vercel
- [ ] Backend deployed (Render/Railway/other)
- [ ] Environment variables configured
- [ ] CORS updated with production URLs
- [ ] API calls working between frontend and backend
- [ ] Can create a quiz
- [ ] Can view quizzes
- [ ] Can delete quizzes
- [ ] Can take a quiz and see results

## 🔍 Testing Your Deployment

1. **Test Frontend**:
   - Visit your Vercel URL
   - Check if the UI loads correctly

2. **Test Backend Connection**:
   - Try creating a quiz
   - Check browser console for any CORS errors
   - Verify API calls in Network tab

3. **Test Full Flow**:
   - Create a quiz
   - View the quiz
   - Take the quiz
   - Delete the quiz

## 🐛 Troubleshooting

### CORS Errors

**Problem**: `Access to fetch has been blocked by CORS policy`

**Solution**:
- Make sure backend CORS includes your Vercel URL
- Redeploy backend after updating CORS
- Clear browser cache

### API Calls Failing

**Problem**: API calls return 404 or timeout

**Solution**:
- Check `VITE_API_URL` environment variable in Vercel
- Verify backend is running (check Render/Railway logs)
- Test backend API directly using curl or Postman

### Build Failures

**Problem**: Vercel build fails

**Solution**:
```bash
# Test build locally first
cd frontend
npm install
npm run build

# Check for errors in build output
```

### Environment Variables Not Working

**Problem**: `VITE_API_URL` is undefined

**Solution**:
- Environment variables must start with `VITE_` in Vite
- Redeploy after adding environment variables in Vercel
- Check spelling and capitalization

## 💰 Cost Breakdown

### Free Tier Resources:

**Vercel (Frontend)**:
- ✅ Free for personal projects
- ✅ Unlimited bandwidth
- ✅ Automatic HTTPS
- ✅ Preview deployments for PRs

**Render (Backend)**:
- ✅ Free tier available
- ⚠️ Spins down after inactivity (cold starts)
- ✅ 750 hours/month free

**Railway (Backend)**:
- ✅ $5 free credit/month
- ✅ No cold starts on paid plans

## 🚀 Continuous Deployment

Both Vercel and Render/Railway support automatic deployments:

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Update quiz platform"
   git push origin main
   ```

2. **Automatic Deployment**:
   - Vercel automatically deploys on push to main
   - Render/Railway also auto-deploys
   - Check deployment status in respective dashboards

## 📝 Quick Commands Reference

```bash
# Push updates to GitHub
git add .
git commit -m "Your message"
git push origin main

# Deploy to Vercel (if using CLI)
vercel --prod

# Check deployment status
vercel ls

# View deployment logs
vercel logs
```

## 🎉 You're Done!

Your Quiz Authoring Platform is now live on Vercel!

**Share your app**: `https://your-project-name.vercel.app`

### Next Steps:
- Monitor error logs in Vercel dashboard
- Set up analytics (Vercel Analytics)
- Add custom domain
- Upgrade database from SQLite to PostgreSQL for production

---

**Need Help?** 
- Vercel Docs: https://vercel.com/docs
- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app
