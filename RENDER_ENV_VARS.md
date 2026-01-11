# Render Environment Variables for Android Backend

## Copy these EXACTLY into Render Dashboard

### Navigate to: Render Dashboard → Your Service → Environment

---

## Required Environment Variables

```bash
# Django Core Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=tars-android-backend.onrender.com

# Database (SAME as website backend - CRITICAL!)
DATABASE_URL=postgresql://neondb_owner:npg_F0AGxH3uream@ep-shy-hat-a8ueooa1-pooler.eastus2.azure.neon.tech/neondb?sslmode=require&channel_binding=require

# Cloudinary (SAME as website backend)
CLOUDINARY_CLOUD_NAME=dfeuvxtao
CLOUDINARY_API_KEY=221856271865514
CLOUDINARY_API_SECRET=y-yyY9XLFWvAUj0ZMGWxhWnKzJU

# CORS & CSRF (Android-specific)
ANDROID_BACKEND_URL=https://tars-android-backend.onrender.com
CSRF_TRUSTED_ORIGINS=https://tars-android-backend.onrender.com

# Render Specific (will be auto-set by Render)
RENDER_EXTERNAL_HOSTNAME=tars-android-backend.onrender.com
```

---

## How to Add in Render

1. Go to: https://dashboard.render.com/
2. Select your `tars-android-backend` service
3. Click **"Environment"** in left sidebar
4. Click **"Add Environment Variable"** for each variable above
5. Copy-paste the **Key** and **Value** exactly as shown
6. Click **"Save Changes"**

---

## ⚠️ CRITICAL Notes

### MUST Use SAME Values:
- ✅ `SECRET_KEY` - Must match website backend
- ✅ `DATABASE_URL` - Must match website backend  
- ✅ All `CLOUDINARY_*` - Must match website backend

### Update These After Deployment:
After your service is deployed, Render will give you a URL like:
`https://tars-android-backend-xyz123.onrender.com`

Update these variables with your actual URL:
- `ALLOWED_HOSTS` → your-actual-url.onrender.com
- `ANDROID_BACKEND_URL` → https://your-actual-url.onrender.com
- `CSRF_TRUSTED_ORIGINS` → https://your-actual-url.onrender.com
- `RENDER_EXTERNAL_HOSTNAME` → your-actual-url.onrender.com

---

## Verification

After deployment, test:
```bash
curl https://your-service-url.onrender.com/api/health/
```

Should return:
```json
{
  "status": "healthy",
  "database": "connected",
  "service": "TARS Backend API - Android"
}
```
