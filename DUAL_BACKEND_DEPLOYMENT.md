# Dual Backend Deployment Guide

## 🏗️ Architecture Overview

This project uses a **dual backend architecture** where:
- **Website Backend** serves the React frontend (Vercel)
- **Android Backend** serves the mobile app (Capacitor)
- **Both backends share the same PostgreSQL database**

This ensures data consistency while allowing platform-specific optimizations.

---

## 📋 Prerequisites

- [x] PostgreSQL database (Neon or Render)
- [x] Cloudinary account (for media storage)
- [x] Two deployment platforms (e.g., 2 Render Web Services)
- [x] GitHub repository

---

## 🗄️ Step 1: Database Setup (One Time)

### Create Shared Database

**Using Neon** (Recommended - Free tier):
1. Go to [neon.tech](https://neon.tech)
2. Create new project: `tars-database`
3. Copy connection string (looks like):
   ```
   postgresql://username:password@ep-xyz.region.aws.neon.tech/tars_db?sslmode=require
   ```
4. **Save this** - both backends will use it!

**Using Render PostgreSQL**:
1. Create new PostgreSQL database on Render
2. Copy Internal/External Connection String
3. **Save this** - both backends will use it!

### Initialize Database (First Time Only)

Choose ONE backend to run initial migrations:

```bash
# In either backend/ or backend-android/
export DATABASE_URL="your-postgresql-url"
python manage.py migrate
python manage.py createsuperuser
```

This creates all tables, and both backends will use them.

---

## 🌐 Step 2: Deploy Website Backend

### Render Deployment

1. **Create Web Service** on Render
   - Name: `tars-backend-web`
   - Root Directory: `backend`
   - Build Command: `./build.sh`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT tars.wsgi:application`

2. **Environment Variables**:
   ```bash
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   DATABASE_URL=postgresql://...  # Your shared database URL
   ALLOWED_HOSTS=tars-backend-web.onrender.com,tars-sage.vercel.app
   
   # CORS - Website origins
   CORS_ALLOWED_ORIGINS=https://tars-sage.vercel.app
   CSRF_TRUSTED_ORIGINS=https://tars-sage.vercel.app,https://tars-backend-web.onrender.com
   
   # Cloudinary
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ```

3. **Deploy** and note the URL: `https://tars-backend-web.onrender.com`

4. **Update Frontend** (`frontend/app/.env.production`):
   ```bash
   VITE_API_URL=https://tars-backend-web.onrender.com
   ```

---

## 📱 Step 3: Deploy Android Backend

### Render Deployment

1. **Create Web Service** on Render
   - Name: `tars-backend-android`
   - Root Directory: `backend-android`
   - Build Command: `./build.sh`
   - Start Command: `gunicorn --bind 0.0.0.0:$PORT tars.wsgi:application`

2. **Environment Variables**:
   ```bash
   SECRET_KEY=same-secret-key-as-website  # MUST BE SAME for JWT
   DEBUG=False
   DATABASE_URL=postgresql://...  # SAME database URL as website backend
   ALLOWED_HOSTS=tars-backend-android.onrender.com
   
   # CORS - Mobile only (NO web origins)
   ANDROID_BACKEND_URL=https://tars-backend-android.onrender.com
   CSRF_TRUSTED_ORIGINS=https://tars-backend-android.onrender.com
   
   # Cloudinary - SAME credentials
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   ```

3. **Deploy** and note the URL: `https://tars-backend-android.onrender.com`

---

## 🔧 Step 4: Configure Android App

### Update Capacitor Config

**File**: `android-app/capacitor.config.json`

```json
{
  "appId": "com.tars.club",
  "appName": "TARS",
  "webDir": "dist",
  "server": {
    "url": "https://tars-backend-android.onrender.com",
    "cleartext": false,
    "androidScheme": "https"
  },
  "android": {
    "allowMixedContent": false
  }
}
```

### Update API Service

**File**: `android-app/src/services/api.ts`

```typescript
const API_BASE_URL = 'https://tars-backend-android.onrender.com';
```

### Update Network Security

**File**: `android-app/android/app/src/main/res/xml/network_security_config.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <domain-config cleartextTrafficPermitted="false">
        <domain includeSubdomains="true">tars-backend-android.onrender.com</domain>
    </domain-config>
</network-security-config>
```

---

## ✅ Step 5: Verification

### Test Website Backend

```bash
# Health check
curl https://tars-backend-web.onrender.com/api/health/

# Should return:
{
  "status": "healthy",
  "service": "TARS Backend API",
  "database": "connected"
}
```

### Test Android Backend

```bash
# Health check
curl https://tars-backend-android.onrender.com/api/health/

# Should return:
{
  "status": "healthy",
  "service": "TARS Backend API - Android",
  "platform": "Android",
  "database": "connected"
}
```

### Test Data Consistency

1. **Login to website backend admin**: `https://tars-backend-web.onrender.com/admin/`
2. **Create a test class** or resource
3. **Check Android backend admin**: `https://tars-backend-android.onrender.com/admin/`
4. **Verify** same data appears (shared database!)
5. **Test in Android app** - data should load

---

## 🔐 Important Security Notes

### Secret Key

**CRITICAL**: Both backends MUST use the **same SECRET_KEY** for JWT authentication to work across platforms.

```bash
# Generate a secure key (once)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Use this SAME key in both backends
```

### CORS Configuration

**Website Backend**:
- Allows: Web frontend origins (Vercel, localhost)
- Blocks: Mobile app schemes

**Android Backend**:
- Allows: Mobile app schemes (capacitor://, https://localhost)
- Blocks: Web frontend origins

This provides **defense in depth** security.

---

## 🔄 Making Changes

### Updating Models

When you modify Django models:

1. **Edit** models in ONE backend (e.g., `backend/core/models.py`)
2. **Generate migration**:
   ```bash
   cd backend
   python manage.py makemigrations
   ```
3. **Copy migration** to other backend:
   ```bash
   cp backend/core/migrations/0006_new_migration.py backend-android/core/migrations/
   ```
4. **Deploy both** backends (they'll run the same migration)

### Updating Views/APIs

If you add new API endpoints:

1. Update in **both** `backend/` and `backend-android/`
2. Keep `views.py`, `serializers.py`, `urls.py` in sync
3. Deploy both backends

---

## 📊 Monitoring

### Check Both Backends

Use UptimeRobot or similar to monitor:
- Website Backend: `https://tars-backend-web.onrender.com/api/health/`
- Android Backend: `https://tars-backend-android.onrender.com/api/health/`

### Database Monitoring

- **Connections**: Both backends share connection pool
- **Watch for**: Connection pool exhaustion (adjust if needed)
- **Neon Dashboard**: Monitor query performance

### Logs

**Render**:
- Check logs in dashboard for each service
- Look for: CORS errors, database connection issues, 500 errors

---

## 🐛 Troubleshooting

### Problem: Android app shows CORS errors

**Solution**: 
- Verify Android backend is deployed with correct CORS settings
- Check `backend-android/tars/settings.py` has Capacitor schemes
- Ensure app is using Android backend URL, not website backend

### Problem: Data not syncing

**Solution**:
- Both backends MUST use same `DATABASE_URL`
- Check database connections in both admin panels
- Verify migrations are run on both backends

### Problem: Login works on web but not app

**Solution**:
- Ensure both backends use **SAME SECRET_KEY**
- Check JWT tokens are being sent correctly from app
- Verify Android backend `/api/auth/login/` endpoint works

### Problem: Images not loading

**Solution**:
- Both backends MUST use same Cloudinary credentials
- Verify `CLOUDINARY_*` env vars are set on both
- Check Cloudinary dashboard for uploaded files

---

## 💰 Cost Optimization

### Free Tier Setup

- **Database**: Neon PostgreSQL (Free tier - 3GB)
- **Website Backend**: Render Web Service (Free tier)
- **Android Backend**: Render Web Service (Free tier)
- **Frontend**: Vercel (Free tier)
- **Media**: Cloudinary (Free tier - 25GB)

**Total Monthly Cost**: $0 (within free tiers)

### Paid Upgrade Path

When you outgrow free tiers:
1. Upgrade Neon database first ($20-50/month)
2. Upgrade Render services as needed ($7-25/month each)
3. Upgrade Cloudinary if needed ($99+/month)

---

## 📈 Scaling Strategy

### Horizontal Scaling

Both backends can scale independently:
- Scale **Website Backend** based on web traffic
- Scale **Android Backend** based on app usage
- Database scales separately

### Vertical Scaling

Upgrade resources as needed:
- Start: 1 instance, 512MB RAM each backend
- Growth: 2-3 instances, 1-2GB RAM each
- Scale: Load balancer + multiple instances

---

## 🎯 Benefits Recap

1. ✅ **Data Consistency**: One database, same data everywhere
2. ✅ **Platform Optimization**: Web vs mobile-specific settings
3. ✅ **Independent Scaling**: Scale web/mobile separately
4. ✅ **Security**: Isolated CORS policies per platform
5. ✅ **Monitoring**: Track web vs mobile metrics separately
6. ✅ **Deployment**: Update one without affecting the other
7. ✅ **Cost Effective**: Shared database, specialized APIs

---

## 📚 Next Steps

After deployment:

1. ✅ Test both backends health endpoints
2. ✅ Verify website loads data correctly
3. ✅ Build and test Android app
4. ✅ Monitor logs for any errors
5. ✅ Set up uptime monitoring
6. ✅ Create backup strategy for database
7. ✅ Document any custom environment variables

---

**Questions?** Check individual README files:
- `backend/README.md` - Website backend docs
- `backend-android/README.md` - Android backend docs
- `android-app/README.md` - Android app docs
