# Backend Comparison: Website vs Android

## Quick Reference Table

| Aspect | Website Backend | Android Backend |
|--------|----------------|-----------------|
| **📁 Location** | `/backend/` | `/backend-android/` |
| **🌐 Port (Dev)** | 8000 | 8001 |
| **🎯 Purpose** | Serves React web app | Serves Capacitor Android app |
| **👥 CORS Origins** | `https://tars-sage.vercel.app`<br>`http://localhost:5173` | `capacitor://localhost`<br>`https://localhost`<br>`ionic://localhost` |
| **🗄️ Database** | PostgreSQL / SQLite | **SAME DATABASE** |
| **📊 Models** | Django models in `core/` | **SAME MODELS** (copied from backend) |
| **🔑 JWT Secret** | `SECRET_KEY` in .env | **MUST BE SAME** as website |
| **🎨 Cloudinary** | Your Cloudinary account | **SAME ACCOUNT** (shared media) |
| **🌐 Deployment** | Render/Heroku | Render/Heroku (separate service) |
| **📍 API Endpoints** | `/api/*` | **SAME ENDPOINTS** |
| **👨‍💼 Admin Panel** | `/admin/` | `/admin/` (separate but same data) |

---

## URL Examples

### Development (Local)

| Service | Website Backend | Android Backend |
|---------|----------------|-----------------|
| **API Base** | `http://localhost:8000` | `http://localhost:8001` |
| **Health Check** | `http://localhost:8000/api/health/` | `http://localhost:8001/api/health/` |
| **Admin** | `http://localhost:8000/admin/` | `http://localhost:8001/admin/` |
| **Login** | `http://localhost:8000/api/auth/login/` | `http://localhost:8001/api/auth/login/` |
| **Classes** | `http://localhost:8000/api/classes/` | `http://localhost:8001/api/classes/` |

### Production

| Service | Website Backend | Android Backend |
|---------|----------------|-----------------|
| **API Base** | `https://tars-bkv7.onrender.com` | `https://your-android-backend.onrender.com` |
| **Health** | `https://tars-bkv7.onrender.com/api/health/` | `https://your-android-backend.onrender.com/api/health/` |
| **Admin** | `https://tars-bkv7.onrender.com/admin/` | `https://your-android-backend.onrender.com/admin/` |

---

## Client Configuration

### React Web App

**File**: `frontend/app/.env.production`
```bash
VITE_API_URL=https://tars-bkv7.onrender.com
```

**Deployed on**: Vercel → `https://tars-sage.vercel.app`

---

### Android App

**File**: `android-app/.env`
```bash
# Local testing
VITE_API_URL=http://10.0.2.2:8001

# Production
VITE_API_URL=https://your-android-backend.onrender.com
```

**File**: `android-app/capacitor.config.json`
```json
{
  "server": {
    "allowNavigation": [
      "https://your-android-backend.onrender.com",
      "http://10.0.2.2:8001"
    ]
  }
}
```

---

## Data Flow Diagram

```
                    USERS
                      │
        ┌─────────────┼─────────────┐
        │                           │
        ▼                           ▼
┌───────────────┐           ┌───────────────┐
│   React Web   │           │ Android App   │
│   Frontend    │           │  (Capacitor)  │
│   (Vercel)    │           │               │
└───────┬───────┘           └───────┬───────┘
        │                           │
        │ API Calls                 │ API Calls
        │                           │
        ▼                           ▼
┌───────────────┐           ┌───────────────┐
│   Website     │           │   Android     │
│   Backend     │           │   Backend     │
│               │           │               │
│ Port: 8000    │           │ Port: 8001    │
│ CORS: Web     │           │ CORS: Mobile  │
└───────┬───────┘           └───────┬───────┘
        │                           │
        └───────────┬───────────────┘
                    │
                    ▼
        ┌───────────────────────┐
        │   PostgreSQL          │
        │   Database            │
        │   (Neon/Render)       │
        │                       │
        │   SHARED DATA:        │
        │   - Users             │
        │   - Classes           │
        │   - Resources         │
        │   - Members           │
        │   - Site Settings     │
        └───────┬───────────────┘
                │
                ▼
        ┌───────────────────────┐
        │   Cloudinary          │
        │   Media Storage       │
        │                       │
        │   SHARED FILES:       │
        │   - Images            │
        │   - Documents         │
        │   - Videos            │
        └───────────────────────┘
```

---

## Environment Variables Comparison

### Website Backend `.env`

```bash
# Django
SECRET_KEY=your-secret-key-12345
DEBUG=False
ALLOWED_HOSTS=tars-bkv7.onrender.com,tars-sage.vercel.app

# Database (Neon PostgreSQL)
DATABASE_URL=postgresql://user:pass@ep-xyz.aws.neon.tech/tars_db

# CORS - Web origins
CORS_ALLOWED_ORIGINS=https://tars-sage.vercel.app
CSRF_TRUSTED_ORIGINS=https://tars-sage.vercel.app,https://tars-bkv7.onrender.com

# Cloudinary
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=123456789
CLOUDINARY_API_SECRET=abc123xyz456
```

### Android Backend `.env`

```bash
# Django - SAME SECRET KEY!
SECRET_KEY=your-secret-key-12345  # ← MUST MATCH
DEBUG=False
ALLOWED_HOSTS=your-android-backend.onrender.com

# Database - SAME DATABASE!
DATABASE_URL=postgresql://user:pass@ep-xyz.aws.neon.tech/tars_db  # ← SAME

# CORS - Mobile only
ANDROID_BACKEND_URL=https://your-android-backend.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-android-backend.onrender.com

# Cloudinary - SAME ACCOUNT!
CLOUDINARY_CLOUD_NAME=your-cloud-name  # ← SAME
CLOUDINARY_API_KEY=123456789          # ← SAME
CLOUDINARY_API_SECRET=abc123xyz456     # ← SAME
```

**⚠️ CRITICAL**: These MUST be the same:
- `SECRET_KEY` (for JWT authentication)
- `DATABASE_URL` (for data consistency)
- `CLOUDINARY_*` (for shared media)

---

## API Response Examples

Both backends return identical data since they share the database.

### GET `/api/health/`

**Website Backend**:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-11T12:00:00Z",
  "service": "TARS Backend API",
  "database": "connected"
}
```

**Android Backend**:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-11T12:00:00Z",
  "service": "TARS Backend API - Android",
  "platform": "Android",
  "database": "connected"
}
```

### GET `/api/classes/`

**Both backends return SAME data**:
```json
[
  {
    "id": 1,
    "title": "Introduction to Web Development",
    "instructor": "John Doe",
    "difficulty": "beginner",
    "start_date": "2026-01-15T10:00:00Z",
    "enrolled_count": 15,
    "max_participants": 30
  }
]
```

---

## Deployment Checklist

### Initial Setup (One Time)

- [ ] Create PostgreSQL database (Neon/Render)
- [ ] Create Cloudinary account
- [ ] Generate secret key
- [ ] Run migrations on one backend

### Website Backend

- [ ] Deploy to Render/Heroku
- [ ] Set environment variables
- [ ] Verify health check works
- [ ] Test API endpoints
- [ ] Update React app with backend URL
- [ ] Deploy React app to Vercel

### Android Backend

- [ ] Deploy to Render/Heroku (separate service)
- [ ] Set environment variables (SAME database & secret!)
- [ ] Verify health check works
- [ ] Test API endpoints
- [ ] Update Android app with backend URL
- [ ] Build and test Android APK

### Verification

- [ ] Both backends respond to health checks
- [ ] Same data appears in both admin panels
- [ ] User can login on website
- [ ] Same user can login on Android app
- [ ] Class created on web appears in app
- [ ] Resource uploaded on web available in app

---

## Cost Breakdown

### Free Tier (Recommended for Start)

| Service | Provider | Cost | Limit |
|---------|----------|------|-------|
| **Database** | Neon | $0/month | 3GB storage, 1 project |
| **Website Backend** | Render | $0/month | Sleeps after inactivity |
| **Android Backend** | Render | $0/month | Sleeps after inactivity |
| **Frontend** | Vercel | $0/month | 100GB bandwidth |
| **Media Storage** | Cloudinary | $0/month | 25GB storage, 25k transformations |
| **Total** | | **$0/month** | Perfect for development |

### Paid Tier (Production)

| Service | Provider | Cost | Benefit |
|---------|----------|------|---------|
| **Database** | Neon | $19/month | 10GB, always on, backups |
| **Website Backend** | Render | $7/month | Always on, no sleep |
| **Android Backend** | Render | $7/month | Always on, no sleep |
| **Frontend** | Vercel | $0/month | Still free! |
| **Media Storage** | Cloudinary | $0-99/month | Based on usage |
| **Total** | | **$33-132/month** | Professional hosting |

---

## Commands Quick Reference

### Website Backend

```bash
cd backend
python manage.py runserver 0.0.0.0:8000     # Start dev server
python manage.py migrate                     # Run migrations
python manage.py createsuperuser             # Create admin
```

### Android Backend

```bash
cd backend-android
python manage.py runserver 0.0.0.0:8001     # Start dev server
python manage.py migrate                     # Run migrations
python manage.py createsuperuser             # Create admin
```

### React App

```bash
cd frontend/app
npm run dev                                  # Development
npm run build                                # Production build
```

### Android App

```bash
cd android-app
npm run build                                # Build web assets
npx cap sync                                 # Sync to Android
npx cap open android                         # Open in Android Studio
```

---

## When to Use Which Backend?

### Use Website Backend

- ✅ Developing React web frontend
- ✅ Testing web application features
- ✅ Managing content via web admin
- ✅ Web browser access
- ✅ Desktop users

### Use Android Backend

- ✅ Developing Android app
- ✅ Testing mobile features
- ✅ Mobile-specific optimizations
- ✅ Android device/emulator access
- ✅ Mobile users

### Use Both

- ✅ Full-stack development
- ✅ Cross-platform data consistency
- ✅ Production deployment
- ✅ Real-time data sync between web and mobile

---

## Summary

**You now have TWO backends, ONE database**:

1. **Website Backend** → For React web app
2. **Android Backend** → For Capacitor mobile app
3. **Shared Database** → Data consistency
4. **Shared Media** → Same Cloudinary files
5. **Same JWT** → Users work on both platforms

This architecture provides:
- ✅ Platform-specific optimizations
- ✅ Independent scaling
- ✅ Better security (isolated CORS)
- ✅ Data consistency (shared database)
- ✅ Easy maintenance (separate deployments)

**Result**: A professional, scalable, full-stack application! 🎉
