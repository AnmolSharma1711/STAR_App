# 🔨 Android App Build Instructions

## Step-by-Step Guide

### 1. Initial Setup (First Time Only)

```bash
# Navigate to android-app folder
cd android-app

# Install dependencies
npm install

# This will:
# - Install frontend dependencies
# - Add Android platform via Capacitor
# - Copy configuration files
npm run android:setup
```

### 2. Build the App

```bash
# Build frontend with production API and sync to Android
npm run android:build
```

This command does:
- Builds the React frontend with `VITE_API_URL=https://tars-bkv7.onrender.com`
- Copies build to Android platform
- Syncs Capacitor

### 3. Open in Android Studio

```bash
npm run cap:open
```

This will:
- Open the project in Android Studio
- You can then run on emulator or physical device

### 4. Build APK (Command Line)

```bash
cd android

# Debug build
./gradlew assembleDebug

# Release build (requires signing)
./gradlew assembleRelease
```

**APK Location:**
- Debug: `android/app/build/outputs/apk/debug/app-debug.apk`
- Release: `android/app/build/outputs/apk/release/app-release.apk`

---

## 🌐 GitHub Actions (Automated Build)

### Setup

1. **Push to GitHub:**
   ```bash
   cd d:/back/TARS
   git add .
   git commit -m "Add Android app build configuration"
   git push origin main
   ```

2. **GitHub Actions will automatically:**
   - Build the APK on every push to `main` or `develop`
   - Upload APK as artifacts
   - Create releases (on main branch)

### Download Built APK

1. Go to GitHub repository
2. Click "Actions" tab
3. Click on the latest workflow run
4. Download "tars-debug-apk" from Artifacts

### Manual Trigger

1. Go to "Actions" tab
2. Select "Build Android APK"
3. Click "Run workflow"
4. Select branch and environment
5. Click "Run workflow"

---

## 🔄 Development Workflow

### For Local Backend Testing

```bash
# 1. Start backend
cd ../backend
python manage.py runserver 0.0.0.0:8000

# 2. Find your local IP
ipconfig  # Windows
# Look for IPv4 Address (e.g., 192.168.198.127)

# 3. Update .env in android-app folder
VITE_API_URL=http://192.168.198.127:8000

# 4. Build and run
npm run android:build
npm run cap:open
```

### For Production Backend

```bash
# .env already has production URL
VITE_API_URL=https://tars-bkv7.onrender.com

# Build and run
npm run android:build
npm run cap:open
```

---

## 🛠️ Common Commands

```bash
# Full build and open
npm run android:dev

# Just build frontend
npm run build

# Just sync Capacitor
npm run cap:sync

# Open Android Studio
npm run cap:open

# Clean rebuild
rm -rf android/
npm run android:setup
npm run android:build
```

---

## ✅ Verification Checklist

Before building, ensure:

- [ ] Node.js installed (`node --version`)
- [ ] Java 17+ installed (`java --version`)
- [ ] Frontend builds successfully (`cd ../frontend/app && npm run build`)
- [ ] Backend is accessible (test in browser: `http://YOUR_IP:8000/api/info/`)
- [ ] `.env` has correct API URL
- [ ] Android Studio installed (for opening/running)

---

## 🎯 Quick Reference

| Command | What it does |
|---------|-------------|
| `npm run android:setup` | Initial setup (first time) |
| `npm run android:build` | Build for production |
| `npm run android:dev` | Build and open Android Studio |
| `npm run cap:open` | Open in Android Studio |
| `cd android && ./gradlew assembleDebug` | Build debug APK |
| `cd android && ./gradlew assembleRelease` | Build release APK |

---

## 📱 Installing APK

### On Physical Device

1. **Enable "Install from Unknown Sources"**
2. **Transfer APK to device**
3. **Open and install**

### Via ADB

```bash
# Install debug build
adb install android/app/build/outputs/apk/debug/app-debug.apk

# Install release build
adb install android/app/build/outputs/apk/release/app-release.apk
```

---

## 🚨 Troubleshooting

### Build Fails

```bash
# Clean and rebuild
cd android
./gradlew clean
cd ..
npm run android:build
```

### Connection Issues

```bash
# Verify backend is running
curl http://YOUR_IP:8000/api/info/

# Check .env has correct URL
cat .env

# Rebuild with new config
npm run android:build
```

### Android Studio Not Found

```bash
# Set CAPACITOR_ANDROID_STUDIO_PATH
export CAPACITOR_ANDROID_STUDIO_PATH="/path/to/Android Studio.app"
npm run cap:open
```

---

## 📞 Support

For detailed help, see:
- [README.md](README.md) - Complete documentation
- [../MOBILE_CONNECTION_GUIDE.md](../MOBILE_CONNECTION_GUIDE.md) - Connection setup
- [../CONNECTION_SETUP_COMPLETE.md](../CONNECTION_SETUP_COMPLETE.md) - Backend configuration
