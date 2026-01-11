# TARS Android Backend

## 📱 Overview

This is a **dedicated backend for the TARS Android app**. It runs independently from the website backend but **shares the same PostgreSQL database**, ensuring data consistency between the web and mobile platforms.

## 🎯 Architecture

```
┌─────────────────┐         ┌──────────────────────┐
│   Website       │         │   Android App        │
│   (React)       │         │   (Capacitor)        │
└────────┬────────┘         └──────────┬───────────┘
         │                             │
         │                             │
         ▼                             ▼
┌─────────────────┐         ┌──────────────────────┐
│ Website Backend │         │ Android Backend      │
│ (Port 8000)     │         │ (Port 8001)          │
│                 │         │                      │
│ - Web CORS      │         │ - Mobile CORS        │
│ - Vercel origin │         │ - Capacitor schemes  │
└────────┬────────┘         └──────────┬───────────┘
         │                             │
         └──────────┬──────────────────┘
                    │
                    ▼
         ┌─────────────────────┐
         │  Shared PostgreSQL  │
         │     Database        │
         │   (Neon/Render)     │
         │                     │
         │ - Users             │
         │ - Classes           │
         │ - Resources         │
         │ - Members           │
         └─────────────────────┘
```

## ✨ Key Features

### Shared Resources
- **Same Database**: Both backends connect to the same PostgreSQL database
- **Same Models**: Identical Django models ensure data consistency
- **Same Cloudinary**: Shared media storage for images and files
- **Same JWT Authentication**: Users can log in from web or app

### Android-Specific Optimizations
- **Mobile CORS**: Configured for Capacitor schemes (`capacitor://`, `https://localhost`)
- **No Web Origins**: Doesn't allow web frontend origins (security)
- **Mobile-friendly**: Optimized for mobile API consumption
- **Independent Deployment**: Can be updated without affecting website

## 🚀 Deployment Options

### Option 1: Render (Recommended)

1. **Create New Web Service** on Render
2. **Connect Repository**: Link to your GitHub repo
3. **Configure Service**:
   - **Root Directory**: `backend-android`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT tars.wsgi:application`
   - **Environment**: Python 3

4. **Environment Variables**:
   ```bash
   SECRET_KEY=your-secret-key
   DEBUG=False
   DATABASE_URL=your-neon-postgresql-url  # SAME as website backend
   ALLOWED_HOSTS=your-android-backend.onrender.com
   
   # Cloudinary (same credentials as website)
   CLOUDINARY_CLOUD_NAME=your-cloud-name
   CLOUDINARY_API_KEY=your-api-key
   CLOUDINARY_API_SECRET=your-api-secret
   
   # CORS
   ANDROID_BACKEND_URL=https://your-android-backend.onrender.com
   CSRF_TRUSTED_ORIGINS=https://your-android-backend.onrender.com
   ```

### Option 2: Docker Deployment

```bash
# Build Docker image
docker build -t tars-android-backend .

# Run container
docker run -d \
  -p 8001:8000 \
  -e DATABASE_URL="your-postgresql-url" \
  -e SECRET_KEY="your-secret-key" \
  -e DEBUG=False \
  -e CLOUDINARY_CLOUD_NAME="your-cloud-name" \
  -e CLOUDINARY_API_KEY="your-api-key" \
  -e CLOUDINARY_API_SECRET="your-api-secret" \
  --name tars-android-backend \
  tars-android-backend
```

### Option 3: Heroku

```bash
# Login to Heroku
heroku login

# Create new app
heroku create tars-android-backend

# Set environment variables
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DATABASE_URL="your-postgresql-url"  # SAME database
heroku config:set DEBUG=False
heroku config:set CLOUDINARY_CLOUD_NAME="your-cloud-name"
heroku config:set CLOUDINARY_API_KEY="your-api-key"
heroku config:set CLOUDINARY_API_SECRET="your-api-secret"

# Deploy
git subtree push --prefix backend-android heroku main
```

## 🔧 Local Development

### Setup

```bash
# Navigate to Android backend
cd backend-android

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your settings

# Run migrations (uses shared database)
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server on port 8001
python manage.py runserver 0.0.0.0:8001
```

### Using Start Scripts

**Windows (PowerShell)**:
```powershell
.\start-server.ps1
```

**Windows (Command Prompt)**:
```cmd
start-backend.bat
```

**Mac/Linux**:
```bash
chmod +x start-server.sh
./start-server.sh
```

## 📱 Update Android App Configuration

Update your Android app's API configuration to point to the new backend:

**File**: `android-app/capacitor.config.json`

```json
{
  "appId": "com.tars.club",
  "appName": "TARS",
  "server": {
    "url": "https://your-android-backend.onrender.com",
    "cleartext": false,
    "androidScheme": "https"
  }
}
```

**File**: `android-app/src/services/api.ts`

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 
                     'https://your-android-backend.onrender.com';
```

## 🔐 Important Notes

### Database Migration
- **First Time**: Run migrations on one backend only (either website or Android)
- **Subsequent**: Both backends will recognize existing migrations
- **Shared Schema**: Changes to models affect both backends

### Security
- Both backends use **same JWT secret key** (users can authenticate on both)
- Android backend **only accepts** Capacitor/mobile origins
- Website backend **only accepts** web frontend origins
- This provides **defense in depth** security

### Data Consistency
- Classes created/updated on website **immediately visible** in app
- Resources uploaded on website **instantly available** in app
- User registrations work on **both platforms**
- All data is **real-time synchronized** via shared database

## 🧪 Testing

### Test Health Endpoint

```bash
# Local
curl http://localhost:8001/api/health/

# Production
curl https://your-android-backend.onrender.com/api/health/
```

Expected Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-11T...",
  "service": "TARS Backend API - Android",
  "platform": "Android",
  "database": "connected"
}
```

### Test API from Android App

1. Build and install Android app
2. Check network requests in Chrome DevTools
3. Verify requests go to Android backend URL
4. Confirm JWT authentication works
5. Verify classes and resources load correctly

## 📊 Monitoring

Both backends should be monitored independently:

- **Uptime**: Use UptimeRobot or Render's built-in monitoring
- **Logs**: Check Render dashboard or use `heroku logs --tail`
- **Database**: Monitor connection pool usage
- **Performance**: Track response times for mobile API calls

## 🆘 Troubleshooting

### CORS Errors in App

**Problem**: App shows CORS errors

**Solution**: Verify Android backend CORS settings in `settings.py`:
```python
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://localhost$",
    r"^capacitor://.*$",
    r"^ionic://.*$",
]
```

### Database Connection Issues

**Problem**: Backend can't connect to database

**Solution**: 
1. Verify `DATABASE_URL` environment variable
2. Check database allows connections from backend IP
3. Ensure SSL mode is set correctly for Neon: `?sslmode=require`

### App Not Loading Data

**Problem**: App shows empty screens

**Solution**:
1. Check backend URL in Capacitor config
2. Verify backend is running (test `/api/health/`)
3. Check JWT token is being sent in requests
4. Review backend logs for errors

## 📝 Maintenance

### Updating Models

When you update Django models:

1. **Make changes** in either `backend/` or `backend-android/core/models.py`
2. **Generate migrations** in one backend: `python manage.py makemigrations`
3. **Copy migration file** to other backend's `core/migrations/`
4. **Run migrations** on both backends: `python manage.py migrate`
5. **Deploy** both backends

### Syncing Code

To sync changes between backends:

```bash
# Copy core app changes
cp -r backend/core/* backend-android/core/

# Copy specific files if needed
cp backend/tars/auth_views.py backend-android/tars/auth_views.py
```

## 🎓 Benefits of This Architecture

1. **Separation of Concerns**: Web and mobile have dedicated backends
2. **Independent Scaling**: Scale mobile backend based on app usage
3. **Security**: Different CORS policies for different platforms
4. **Flexibility**: Update mobile backend without affecting website
5. **Monitoring**: Track web vs mobile API usage separately
6. **Data Consistency**: Shared database ensures same data everywhere
7. **Cost Effective**: One database, multiple specialized backends

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Render Deployment Guide](https://render.com/docs/deploy-django)
- [Capacitor Configuration](https://capacitorjs.com/docs/config)
- [CORS Configuration](https://pypi.org/project/django-cors-headers/)

---

**Need Help?** Check the main project README or open an issue on GitHub.
