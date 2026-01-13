# Quick Start: Android Backend

## 🚀 Local Development (5 minutes)

### 1. Setup Environment

```bash
cd backend-android
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 2. Configure Database

Create `.env` file:

```bash
# For local testing with SQLite (easiest)
USE_SQLITE=True
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

OR use shared PostgreSQL database:

```bash
# Connect to same database as website
DATABASE_URL=postgresql://user:pass@host:port/dbname
SECRET_KEY=same-as-website-backend
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3. Run Migrations

```bash
python manage.py migrate
python manage.py createsuperuser  # Optional
```

### 4. Start Server

```bash
# Windows
.\start-backend.bat

# Mac/Linux
chmod +x start-server.sh
./start-server.sh
```

Server runs on: `http://localhost:8001`

### 5. Test

```bash
curl http://localhost:8001/api/health/
```

---

## 📱 Update Android App

### Capacitor Config

**File**: `android-app/capacitor.config.json`

For **local testing**:
```json
{
  "server": {
    "url": "http://10.0.2.2:8001",  // Android emulator
    "cleartext": true,
    "androidScheme": "http"
  }
}
```

For **production**:
```json
{
  "server": {
    "url": "https://your-android-backend.onrender.com",
    "cleartext": false,
    "androidScheme": "https"
  }
}
```

### API Service

**File**: `android-app/src/services/api.ts`

```typescript
const API_BASE_URL = 'http://10.0.2.2:8001';  // Local
// const API_BASE_URL = 'https://your-backend.onrender.com';  // Prod
```

---

## ☁️ Quick Deploy to Render

### 1. Create Web Service
- Go to [render.com](https://render.com)
- **New** → **Web Service**
- Connect your GitHub repo

### 2. Configure Service
- **Name**: `tars-android-backend`
- **Root Directory**: `backend-android`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT tars.wsgi:application`

### 3. Add Environment Variables

```bash
SECRET_KEY=copy-from-website-backend
DEBUG=False
DATABASE_URL=copy-from-website-backend
ALLOWED_HOSTS=your-app.onrender.com

CLOUDINARY_CLOUD_NAME=copy-from-website
CLOUDINARY_API_KEY=copy-from-website
CLOUDINARY_API_SECRET=copy-from-website

ANDROID_BACKEND_URL=https://your-app.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com
```

### 4. Deploy!

Click "Create Web Service" - done in ~5 minutes!

---

## ✅ Verification Checklist

- [ ] Backend running locally on port 8001
- [ ] `/api/health/` returns `{"status": "healthy"}`
- [ ] Admin accessible at `/admin/`
- [ ] Can log in with superuser
- [ ] See same data as website backend
- [ ] Android app can connect to backend
- [ ] Android app can fetch classes
- [ ] Android app can fetch resources
- [ ] Login works in Android app
- [ ] JWT tokens work across platforms

---

## 🔑 Key Points

### Same Database = Same Data
Both backends see identical:
- Users
- Classes  
- Resources
- Members
- Team Members
- All other models

### Same Secret Key = Same JWT
Users can log in from:
- Website → get token → use in app ✅
- App → get token → use on website ✅

### Different CORS = Better Security
- Website backend: Only allows web origins
- Android backend: Only allows mobile schemes

---

## 📞 Common Commands

### Development
```bash
python manage.py runserver 0.0.0.0:8001
```

### Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Admin
```bash
python manage.py createsuperuser
```

### Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Shell
```bash
python manage.py shell
```

---

## 🆘 Quick Troubleshooting

### Can't connect to database
→ Check `DATABASE_URL` in `.env`

### CORS errors in app  
→ Verify Capacitor schemes in `settings.py`

### Login not working
→ Ensure `SECRET_KEY` matches website backend

### No data showing
→ Check database has data (use admin panel)

### Port already in use
→ Kill process: `netstat -ano | findstr :8001` (Windows)

---

## 📚 Full Documentation

- **Complete Setup**: [DUAL_BACKEND_DEPLOYMENT.md](../DUAL_BACKEND_DEPLOYMENT.md)
- **Detailed Guide**: [README.md](README.md)
- **Website Backend**: [../backend/README.md](../backend/README.md)

---

**Ready?** Start with `cd backend-android && .\start-backend.bat` 🚀
