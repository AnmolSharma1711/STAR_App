# GitHub Actions Deployment Guide

## 🎯 Complete Setup Instructions

### Step 1: Configure GitHub Secrets

1. **Go to your repository**: https://github.com/AnmolSharma1711/STAR_App

2. **Navigate to**: Settings → Secrets and variables → Actions

3. **Click**: "New repository secret"

4. **Add this secret**:
   ```
   Name: ANDROID_BACKEND_URL
   Value: https://tars-android-backend.onrender.com
   ```
   
   (Update with your actual Render URL after deployment)

### Step 2: Push GitHub Actions Workflows

The workflows are already created. Now push them:

```bash
cd D:\back\TARS
git add .github/
git commit -m "Add GitHub Actions for Android builds"
git push star main
```

### Step 3: Trigger Your First Build

**Option A: Automatic (Recommended)**
```bash
# Any push to main will trigger a build
git add .
git commit -m "Trigger first Android build"
git push star main
```

**Option B: Manual**
1. Go to: https://github.com/AnmolSharma1711/STAR_App/actions
2. Select "Build Android APK" workflow
3. Click "Run workflow" button
4. Select "main" branch
5. Click "Run workflow"

### Step 4: Monitor Build Progress

1. Go to: https://github.com/AnmolSharma1711/STAR_App/actions
2. Click on the running workflow
3. Watch the build progress (takes ~10-15 minutes)
4. Check for green checkmarks ✅

### Step 5: Download Your APK

After build completes:

**From Artifacts**:
1. Scroll down to "Artifacts" section
2. Click "app-debug" to download debug APK
3. Click "app-release" to download release APK

**From Releases** (if tagged):
1. Go to: https://github.com/AnmolSharma1711/STAR_App/releases
2. Download latest APK

---

## 📱 How GitHub Actions Works

### Automatic Builds

Every time you push code, GitHub Actions will:

```
1. Checkout your code
2. Setup Node.js and Java
3. Install dependencies
4. Build React frontend (frontend/app/)
5. Copy build to android-app/dist
6. Sync Capacitor
7. Build Android APK
8. Upload APK to Artifacts
9. Create GitHub Release (on main branch)
```

### Build Triggers

| Action | Trigger | Result |
|--------|---------|--------|
| `git push` | Any push to main | Debug + Release APKs |
| `git tag v1.0.0` | Version tag | Production release |
| Manual | Click "Run workflow" | On-demand build |

---

## 🚀 Complete Deployment Process

### 1. Deploy Backend to Render

```bash
# Already done! Your backend is in the repo
# Just deploy on Render with these settings:
```

**Render Configuration**:
- Name: `tars-android-backend`
- Root Directory: `backend-android`
- Build Command: `./build.sh`
- Start Command: `gunicorn --bind 0.0.0.0:$PORT tars.wsgi:application`

**Environment Variables** (copy from RENDER_ENV_VARS.md):
```bash
SECRET_KEY=jkdowuel!42%+qxhd&)!o_4qwbc0%3*^k+h*^62csho4)m1ol2
DATABASE_URL=postgresql://neondb_owner:npg_F0AGxH3uream@ep-shy-hat-a8ueooa1-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require
CLOUDINARY_CLOUD_NAME=dfeuvxtao
CLOUDINARY_API_KEY=221856271865514
CLOUDINARY_API_SECRET=y-yyY9XLFWvAUj0ZMGWxhWnKzJU
DEBUG=False
ALLOWED_HOSTS=your-url.onrender.com
ANDROID_BACKEND_URL=https://your-url.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-url.onrender.com
```

### 2. Update Android App Configuration

After backend is deployed, update the backend URL:

**Update GitHub Secret**:
1. Go to: Settings → Secrets → ANDROID_BACKEND_URL
2. Update with your actual Render URL

**Update capacitor.config.json**:
```json
{
  "server": {
    "url": "https://your-actual-url.onrender.com"
  }
}
```

### 3. Trigger Build

```bash
git add android-app/capacitor.config.json
git commit -m "Update backend URL"
git push star main
```

### 4. Download and Test APK

1. Wait for build to complete (~10 min)
2. Go to Actions → Download artifact
3. Install APK on Android device
4. Test app functionality

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

### Backend
- [ ] Backend code pushed to GitHub
- [ ] Render service created
- [ ] Environment variables configured
- [ ] Database connection working
- [ ] Health endpoint returns success

### GitHub
- [ ] GitHub Actions workflows pushed
- [ ] `ANDROID_BACKEND_URL` secret added
- [ ] Repository has Actions enabled

### App Configuration
- [ ] `capacitor.config.json` has correct backend URL
- [ ] `.env` file created with API URL
- [ ] Network security config updated

---

## 🔄 Continuous Deployment Workflow

### Daily Development
```bash
# Make changes to your code
code frontend/app/src/components/Home.tsx

# Test locally
cd frontend/app
npm run dev

# Commit and push
git add .
git commit -m "Update home page"
git push star main

# ✨ GitHub Actions automatically builds APK
# Download from Actions → Artifacts
```

### Creating Releases
```bash
# When ready for new version
git tag v1.0.0
git push star v1.0.0

# ✨ GitHub Actions creates release with APK
# Download from Releases page
```

---

## 📱 APK Distribution Options

### Option 1: Direct Download (Easiest)
1. Share GitHub Releases link
2. Users download APK
3. Users enable "Unknown Sources"
4. Users install APK

### Option 2: Firebase App Distribution
- Upload APK to Firebase
- Invite testers via email
- Automatic updates for testers

### Option 3: Google Play Store (Most Professional)
- Sign APK with production keystore
- Create Play Store listing
- Submit for review
- Publish to millions of users

---

## 🎬 Quick Start Commands

### Push Everything to GitHub
```bash
cd D:\back\TARS

# Add all new files
git add .github/ RENDER_ENV_VARS.md GITHUB_ACTIONS_SETUP.md

# Commit
git commit -m "Add GitHub Actions workflows and deployment docs"

# Push to your repo
git push star main
```

### Set Up GitHub Secret
```bash
# Go to: https://github.com/AnmolSharma1711/STAR_App/settings/secrets/actions
# Click: "New repository secret"
# Name: ANDROID_BACKEND_URL
# Value: https://your-render-url.onrender.com
# Click: "Add secret"
```

### Trigger First Build
```bash
# Either push any change:
git commit --allow-empty -m "Trigger first build"
git push star main

# Or use manual trigger on GitHub Actions page
```

---

## ✅ Success Indicators

You'll know everything is working when:

### Backend
- ✅ Render deployment succeeds
- ✅ Health endpoint returns healthy
- ✅ Admin panel accessible
- ✅ Database connected

### GitHub Actions
- ✅ Workflow runs without errors
- ✅ All steps show green checkmarks
- ✅ APK available in Artifacts
- ✅ Release created automatically

### Android App
- ✅ APK installs on device
- ✅ App opens successfully
- ✅ Backend connection works
- ✅ Classes and resources load
- ✅ Login functionality works

---

## 🆘 Troubleshooting

### Build Fails with "Module not found"
**Solution**: Check `frontend/app/package.json` dependencies
```bash
cd frontend/app
npm install
git add package-lock.json
git commit -m "Update dependencies"
git push
```

### APK Won't Install
**Solution**: Enable "Unknown Sources" in Android settings
- Settings → Security → Unknown Sources → Enable

### App Shows "Network Error"
**Solution**: 
1. Check backend is running: `curl https://your-url.onrender.com/api/health/`
2. Verify ANDROID_BACKEND_URL secret matches actual URL
3. Rebuild APK after updating secret

### Build Takes Too Long
**Normal**: First build takes 15-20 minutes
**Subsequent**: 5-10 minutes (uses cache)

---

## 🎉 You're All Set!

### What You Have Now:

1. ✅ **Backend Code** - Ready to deploy on Render
2. ✅ **GitHub Actions** - Automatic APK builds
3. ✅ **Documentation** - Complete setup guides
4. ✅ **Environment Config** - Production-ready settings

### What to Do Next:

1. **Deploy Backend to Render** (10 minutes)
2. **Add GitHub Secret** (2 minutes)  
3. **Push to GitHub** (1 minute)
4. **Wait for Build** (10 minutes)
5. **Download APK** (1 minute)
6. **Install and Test** (5 minutes)

**Total Time: ~30 minutes to fully deployed app!** 🚀

---

## 📚 Documentation Index

- **RENDER_ENV_VARS.md** - Exact Render environment variables
- **.github/workflows/README.md** - GitHub Actions documentation
- **ANDROID_BACKEND_COMPLETE.md** - Complete backend setup
- **DUAL_BACKEND_DEPLOYMENT.md** - Deployment guide
- **BACKEND_COMPARISON.md** - Backend comparison

---

**Ready to deploy?** Start with deploying the backend to Render! 🎯
