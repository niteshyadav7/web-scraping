# Render.com Deployment Guide

## 🚀 Complete Step-by-Step Guide

### Prerequisites
- ✅ GitHub account
- ✅ Render.com account (free)
- ✅ Your code ready to deploy

---

## Part 1: Prepare Your Code for Deployment

### ✅ Files Created (Already Done!)

The following files have been created for you:

1. **`Procfile`** - Tells Render how to run your app
2. **`requirements.txt`** - Python dependencies (updated with gunicorn)
3. **`render-build.sh`** - Installs Chrome and ChromeDriver
4. **`runtime.txt`** - Specifies Python version
5. **`api.py`** - Updated for production (host='0.0.0.0')

---

## Part 2: Push Code to GitHub

### Step 1: Initialize Git Repository

```powershell
# Navigate to your project
cd "d:\yash\New folder\flipkart_scraper"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Prepare for Render.com deployment"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com
2. Click **"New Repository"**
3. Name: `flipkart-scraper`
4. Visibility: **Public** or **Private** (both work)
5. Click **"Create repository"**

### Step 3: Push to GitHub

```powershell
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/flipkart-scraper.git

# Push code
git branch -M main
git push -u origin main
```

---

## Part 3: Deploy Backend to Render.com

### Step 1: Create Render Account

1. Go to https://render.com
2. Click **"Get Started for Free"**
3. Sign up with GitHub (easiest)
4. Authorize Render to access your repositories

### Step 2: Create New Web Service

1. Click **"New +"** button
2. Select **"Web Service"**
3. Connect your GitHub repository: `flipkart-scraper`
4. Click **"Connect"**

### Step 3: Configure Web Service

Fill in the following settings:

| Field | Value |
|-------|-------|
| **Name** | `flipkart-scraper-api` |
| **Region** | Choose closest to you |
| **Branch** | `main` |
| **Root Directory** | *(leave empty)* |
| **Runtime** | `Python 3` |
| **Build Command** | `bash render-build.sh` |
| **Start Command** | `gunicorn api:app` |
| **Instance Type** | **Free** |

### Step 4: Add Environment Variables

Click **"Advanced"** and add:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `PORT` | `10000` (auto-set by Render) |

### Step 5: Deploy!

1. Click **"Create Web Service"**
2. Wait for deployment (5-10 minutes first time)
3. Watch the build logs

---

## Part 4: Verify Deployment

### Step 1: Check Build Logs

You should see:
```
Installing Chrome...
Installing ChromeDriver...
Installing Python dependencies...
Build complete!
Starting server...
```

### Step 2: Get Your API URL

After deployment, you'll get a URL like:
```
https://flipkart-scraper-api.onrender.com
```

### Step 3: Test the API

Open in browser:
```
https://flipkart-scraper-api.onrender.com/api/status
```

You should see:
```json
{
  "is_running": false,
  "current_page": 0,
  "total_reviews": 0,
  "status": "idle",
  ...
}
```

✅ **If you see this, your backend is deployed!**

---

## Part 5: Update Frontend to Use Deployed Backend

### Update API URL in Frontend

Edit `frontend/src/App.jsx`:

```javascript
// Change this line:
const API_URL = 'http://localhost:5000'

// To this (use your Render URL):
const API_URL = 'https://flipkart-scraper-api.onrender.com'
```

### Test Locally

```powershell
cd frontend
npm run dev
```

Try scraping - it should now use the deployed backend!

---

## Part 6: Deploy Frontend (Optional)

### Option A: Deploy to Render (Static Site)

1. In Render dashboard, click **"New +"**
2. Select **"Static Site"**
3. Connect same repository
4. Configure:
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
5. Deploy!

### Option B: Deploy to Firebase Hosting

```powershell
# Install Firebase CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize
cd frontend
firebase init hosting

# Build
npm run build

# Deploy
firebase deploy --only hosting
```

---

## 🎯 Important Notes

### ⚠️ **Free Tier Limitations**

**Render Free Tier**:
- ✅ 750 hours/month
- ⚠️ Spins down after 15 min inactivity
- ⚠️ Cold start: 15-30 seconds
- ⚠️ 512 MB RAM
- ⚠️ Shared CPU

**What this means**:
- First request after inactivity will be slow
- Large scraping jobs might timeout
- May need to reduce max_pages

### 🔧 **Optimization Tips**

1. **Reduce Max Pages**: Use 20-50 instead of 500
2. **Smaller Batches**: Scrape fewer products at once
3. **Keep Alive**: Ping your API every 10 minutes to prevent sleep

### 🐛 **Troubleshooting**

**Build Fails**:
- Check build logs in Render dashboard
- Ensure `render-build.sh` has correct permissions
- Verify all files are pushed to GitHub

**Chrome Not Found**:
- Check if build script ran successfully
- Look for "Installing Chrome..." in logs
- May need to update Chrome installation commands

**Timeout Errors**:
- Reduce max_pages
- Scrape fewer products
- Consider upgrading to paid tier

---

## 📊 **Cost Breakdown**

| Service | Cost | What You Get |
|---------|------|--------------|
| **Render Free** | $0/month | 750 hours, 512MB RAM |
| **Render Starter** | $7/month | Always on, 512MB RAM |
| **Render Standard** | $25/month | 2GB RAM, better performance |

**Recommendation**: Start with free tier, upgrade if needed.

---

## 🎉 **You're Done!**

Your scraper is now deployed and accessible from anywhere!

**Your URLs**:
- Backend API: `https://flipkart-scraper-api.onrender.com`
- Frontend: `https://your-frontend-url.onrender.com` (if deployed)

**Next Steps**:
1. Share the frontend URL with others
2. Monitor usage in Render dashboard
3. Check logs if issues occur
4. Consider upgrading if you need better performance

---

## 📞 **Need Help?**

**Common Issues**:
- Build fails → Check GitHub repo has all files
- Chrome errors → Check build logs
- Timeout → Reduce max_pages
- Slow response → Normal for free tier (cold start)

**Render Documentation**:
https://render.com/docs

---

**Happy Deploying! 🚀**
