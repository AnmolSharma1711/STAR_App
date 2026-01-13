# GitHub Actions Setup for TARS Android App

This repository includes automated GitHub Actions workflows for building Android APKs.

## 🔧 Setup Required

### 1. Add GitHub Secrets

Go to: **Repository → Settings → Secrets and variables → Actions → New repository secret**

Add the following secrets:

| Secret Name | Value | Description |
|-------------|-------|-------------|
| `ANDROID_BACKEND_URL` | `https://your-backend.onrender.com` | Your deployed Android backend URL |
| `KEYSTORE_PASSWORD` | (optional) | Password for your Android keystore |
| `KEY_ALIAS` | (optional) | Alias for your signing key |
| `KEY_PASSWORD` | (optional) | Password for your signing key |

### 2. Workflows Available

#### `build-android.yml` - Continuous Build
- **Triggers**: On every push to `main` or pull request
- **Builds**: Debug and Release APKs
- **Uploads**: APKs as artifacts
- **Auto-creates**: GitHub Releases with APKs

#### `release-apk.yml` - Version Releases
- **Triggers**: When you push a git tag like `v1.0.0`
- **Builds**: Production release APK
- **Creates**: GitHub Release with version number
- **Downloads**: Get APK from Releases page

## 📱 How to Use

### Automatic Builds (Every Push)

Just push your code:
```bash
git add .
git commit -m "Update app"
git push
```

GitHub Actions will:
1. ✅ Build the frontend
2. ✅ Sync with Capacitor
3. ✅ Build Android APK
4. ✅ Upload to Artifacts

**Download APK**: 
- Go to **Actions** tab → Select workflow run → **Artifacts** section → Download APK

### Create Version Release

When ready to release a new version:

```bash
# Tag your release
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions will:
1. ✅ Build production APK
2. ✅ Create GitHub Release
3. ✅ Attach APK to release

**Download APK**:
- Go to **Releases** tab → Latest release → Download APK

### Manual Trigger

You can also trigger builds manually:
1. Go to **Actions** tab
2. Select **Build Android APK** workflow
3. Click **Run workflow**
4. Choose branch and click **Run**

## 📦 Build Outputs

After successful build:

### Debug APK
- **File**: `app-debug.apk`
- **Size**: ~20-30 MB
- **Use**: Testing and development
- **Signed**: With debug keystore

### Release APK
- **File**: `app-release-unsigned.apk` (or signed if configured)
- **Size**: ~15-25 MB (smaller due to optimization)
- **Use**: Production deployment
- **Signed**: Unsigned (needs signing for Play Store)

## 🔐 APK Signing (Optional)

For Play Store deployment, you need to sign the APK:

### Generate Keystore (One Time)

```bash
cd android-app/android/app
keytool -genkey -v -keystore tars-release-key.keystore -alias tars-key -keyalg RSA -keysize 2048 -validity 10000
```

### Add to GitHub Secrets

1. Convert keystore to base64:
   ```bash
   base64 tars-release-key.keystore > keystore.b64
   ```

2. Add secrets:
   - `KEYSTORE_FILE`: Content of `keystore.b64`
   - `KEYSTORE_PASSWORD`: Your keystore password
   - `KEY_ALIAS`: Your key alias (e.g., `tars-key`)
   - `KEY_PASSWORD`: Your key password

### Update Signing Config

The workflow will automatically sign the APK when secrets are present.

## 📊 Workflow Status

Check build status in your README:

```markdown
![Build Android APK](https://github.com/AnmolSharma1711/STAR_App/actions/workflows/build-android.yml/badge.svg)
```

## 🐛 Troubleshooting

### Build Fails

**Check**:
1. GitHub Actions logs for specific error
2. Ensure `ANDROID_BACKEND_URL` secret is set
3. Verify Node.js and Java versions
4. Check if frontend builds locally

### APK Not Found

**Solution**:
- Wait for workflow to complete (5-10 minutes)
- Check **Actions** tab for progress
- Download from **Artifacts** section after completion

### Backend Connection Error

**Solution**:
- Verify `ANDROID_BACKEND_URL` secret matches your deployed backend
- Ensure backend is running and healthy
- Check backend CORS settings allow Capacitor

## 📝 Customization

### Change Node/Java Versions

Edit `.github/workflows/build-android.yml`:

```yaml
- name: Setup Node.js
  uses: actions/setup-node@v4
  with:
    node-version: '20'  # Change version here

- name: Setup JDK
  uses: actions/setup-java@v4
  with:
    java-version: '17'  # Change version here
```

### Change Trigger Conditions

Edit the `on:` section:

```yaml
on:
  push:
    branches: [ main, develop ]  # Add more branches
  schedule:
    - cron: '0 0 * * 0'  # Weekly builds
```

## 🚀 Deployment Workflow

### Development
1. Code changes → Push to `main`
2. Automatic build triggers
3. Download debug APK from Artifacts
4. Test on device/emulator

### Production Release
1. Test thoroughly
2. Create version tag: `git tag v1.0.0`
3. Push tag: `git push origin v1.0.0`
4. Automatic release created
5. Download from Releases page
6. Distribute to users

## 📱 Distribution

### Direct Distribution
Share the APK file directly with users who can:
1. Enable "Unknown Sources" in Android settings
2. Download and install APK

### Google Play Store
1. Sign APK with production keystore
2. Create Play Store listing
3. Upload signed APK
4. Submit for review

## ✅ Success Indicators

Build is successful when:
- ✅ Workflow status shows green checkmark
- ✅ APK available in Artifacts/Releases
- ✅ APK installs on Android device
- ✅ App connects to backend
- ✅ Data loads correctly

---

**Next Steps**: 
1. Add `ANDROID_BACKEND_URL` secret to GitHub
2. Push code to trigger first build
3. Download and test APK
