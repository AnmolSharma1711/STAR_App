# 🚀 Multi-Platform Connection Setup

This guide explains how to connect your TARS frontend (web & Android app) to the backend.

## 📋 Quick Overview

Your local IPs detected:
- `192.168.56.1`
- `192.168.198.127`

**Use the IP that's on your main network (usually the second one for WiFi)**

---

## 🌐 Configuration Files Summary

### Backend (.env)
✅ **Already Updated** - Supports connections from:
- Local development (localhost)
- Local network (your IP addresses)
- Android app (Capacitor schemes)
- Production frontend (Vercel)

### Frontend Environment Files
Three environment files for different scenarios:

1. **`.env.local`** - Local browser development
2. **`.env.android`** - Android app development  
3. **`.env.production`** - Production deployment

---

## 🔧 Setup Instructions

### 1️⃣ Web Frontend (Browser)

**For development:**
```bash
cd frontend/app
npm run dev
```
Uses: `http://localhost:8000` (automatically)

**For production:**
```bash
npm run build:production
npm run preview
```
Uses: `https://tars-bkv7.onrender.com`

---

### 2️⃣ Android App (Capacitor)

#### Initial Setup (First Time Only)

```bash
cd frontend/app

# Install Capacitor if not already installed
npm install @capacitor/core @capacitor/cli @capacitor/android

# Initialize Capacitor (if not done)
npx cap init

# Add Android platform
npx cap add android
```

#### Configure Android Network Security

After running `npx cap add android`, you need to allow HTTP connections for local development:

**Create:** `android/app/src/main/res/xml/network_security_config.xml`
```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="true">
        <domain includeSubdomains="true">192.168.198.127</domain>
        <domain includeSubdomains="true">192.168.56.1</domain>
        <domain includeSubdomains="true">10.0.2.2</domain>
        <domain includeSubdomains="true">localhost</domain>
    </domain-config>
    <base-config cleartextTrafficPermitted="false" />
</network-security-config>
```

**Update:** `android/app/src/main/AndroidManifest.xml`
```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <!-- Add these permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    
    <application
        android:networkSecurityConfig="@xml/network_security_config"
        android:usesCleartextTraffic="true"
        ...>
        ...
    </application>
</manifest>
```

#### Building for Android

**Local Development (with your local backend):**
```bash
# Make sure .env.android has: VITE_API_URL=http://192.168.198.127:8000
npm run build:android
npx cap sync
npx cap open android
```

**Production (with Render backend):**
```bash
# Edit .env.android to: VITE_API_URL=https://tars-bkv7.onrender.com
npm run build:production
npx cap sync
npx cap open android
```

---

### 3️⃣ Backend Server

#### Local Development

**Option A: Direct Python**
```bash
cd backend
python manage.py runserver 0.0.0.0:8000
```

**Option B: Docker**
```bash
# From project root
docker-compose up
```

The backend will be accessible at:
- `http://localhost:8000` (from your computer)
- `http://192.168.198.127:8000` (from your phone/other devices)

---

## 🧪 Testing Connectivity

### Test Backend is Accessible

**From your computer:**
```bash
curl http://localhost:8000/api/info/
```

**From your phone's browser:**
1. Connect phone to same WiFi network
2. Open browser and visit: `http://192.168.198.127:8000/api/info/`
3. You should see JSON response

If you can't access it from your phone:
- Check firewall settings
- Verify both devices on same network
- Try the other IP address: `http://192.168.56.1:8000/api/info/`

### Test Android App

1. Build and open in Android Studio:
   ```bash
   npm run build:android
   npx cap sync
   npx cap open android
   ```

2. Run on emulator or physical device

3. Check Logcat for network errors:
   - Filter by "chromium" or "TarsApp"
   - Look for CORS or connection errors

---

## 🔍 Troubleshooting

### Problem: Android app shows "Network Error"

**Solution 1:** Verify backend URL in app
- Check `.env.android` has correct IP
- Rebuild: `npm run build:android && npx cap sync`

**Solution 2:** Test backend from phone browser first
- Visit `http://YOUR_IP:8000/api/info/` in phone's browser
- If this fails, it's a network issue, not app issue

**Solution 3:** Check Android network config
- Verify `network_security_config.xml` exists
- Verify `AndroidManifest.xml` references it
- Check IP addresses match your actual IP

### Problem: CORS errors

**Solution:** Backend `.env` already updated with all required origins. If still getting CORS errors:
1. Restart Django server
2. Clear app cache/data
3. Verify `CORS_ALLOWED_ORIGINS` in [.env](backend/.env)

### Problem: Connection refused

**Solution:** Check firewall
```powershell
# Allow Python through Windows Firewall
netsh advfirewall firewall add rule name="Django Dev Server" dir=in action=allow protocol=TCP localport=8000
```

---

## 📱 Production Deployment

### Web Frontend (Vercel)
Already configured! Uses: `https://tars-bkv7.onrender.com`

### Android App (Play Store)
```bash
# 1. Update .env.android for production
echo VITE_API_URL=https://tars-bkv7.onrender.com > .env.android

# 2. Build production bundle
npm run build:production
npx cap sync

# 3. Open Android Studio
npx cap open android

# 4. In Android Studio:
#    - Build > Generate Signed Bundle/APK
#    - Follow Google Play signing process
```

**Important for Production:**
- Remove or restrict `network_security_config.xml` cleartext permissions
- Use HTTPS only
- Update `capacitor.config.ts` to remove `cleartext: true`

---

## 📋 Environment Variables Reference

### `.env.local` (Web Development)
```env
VITE_API_URL=http://localhost:8000
```

### `.env.android` (Android Development)
```env
VITE_API_URL=http://192.168.198.127:8000
```

### `.env.production` (Production)
```env
VITE_API_URL=https://tars-bkv7.onrender.com
```

---

## ✅ Checklist

Before running Android app:
- [ ] Backend is running and accessible
- [ ] Tested backend URL in phone browser
- [ ] `.env.android` has correct IP address
- [ ] Built app: `npm run build:android`
- [ ] Synced Capacitor: `npx cap sync`
- [ ] Created `network_security_config.xml`
- [ ] Updated `AndroidManifest.xml`
- [ ] Phone and computer on same WiFi

---

## 🆘 Still Having Issues?

1. **Check your actual IP:**
   ```powershell
   ipconfig
   ```
   Look for "IPv4 Address" under your active network adapter

2. **Test backend accessibility:**
   ```bash
   curl http://YOUR_IP:8000/api/info/
   ```

3. **Check Django logs** for incoming requests

4. **Enable verbose logging** in Android Studio Logcat

---

Need more help? See [ANDROID_SETUP.md](ANDROID_SETUP.md) for detailed Android configuration.
