# TARS Android App

This folder contains the Android app configuration and build setup for TARS.

## 📁 Structure

```
android-app/
├── android/                          # Capacitor Android platform (auto-generated)
│   ├── app/
│   │   └── src/main/
│   │       ├── AndroidManifest.xml   # App manifest with permissions
│   │       └── res/xml/
│   │           └── network_security_config.xml  # Network security
├── capacitor.config.json             # Capacitor configuration
├── package.json                      # Android build scripts
├── setup-android-configs.js          # Config setup script
└── .env                              # Environment variables
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ installed
- Java 17+ installed (for Android builds)
- Android Studio (optional, for running in emulator)

### Initial Setup

```bash
cd android-app

# Install dependencies
npm install

# Install frontend dependencies and add Android platform
npm run android:setup

# Build the app
npm run android:build

# Open in Android Studio
npm run cap:open
```

## 📋 Available Commands

### Development
```bash
# Build frontend and sync to Android
npm run android:dev

# Build for Android (production)
npm run android:build

# Open in Android Studio
npm run cap:open
```

### Individual Steps
```bash
# Install frontend dependencies
npm run install:app

# Build frontend
npm run build

# Build for Android with production API
npm run build:android

# Sync Capacitor
npm run cap:sync

# Setup Android configs
npm run setup:configs
```

## 🔧 Configuration

### Environment Variables (.env)

```env
# Production (default)
VITE_API_URL=https://tars-bkv7.onrender.com

# Local Development
# VITE_API_URL=http://192.168.198.127:8000
```

### API Endpoints

The app is configured to connect to:
- **Production:** `https://tars-bkv7.onrender.com`
- **Local Development:** `http://YOUR_LOCAL_IP:8000`

### Network Security

The app allows HTTP connections to:
- `192.168.x.x` (local network)
- `10.0.2.2` (Android emulator)
- `localhost` / `127.0.0.1`

For production builds, only HTTPS connections are allowed except for the above local IPs.

## 🏗️ Building with GitHub Actions

The repository includes a GitHub Actions workflow that automatically builds the APK on every push to `main` or `develop`.

### Workflow File
`.github/workflows/build-android.yml`

### Triggers
- Push to `main` or `develop` branches
- Pull requests to `main`
- Manual workflow dispatch

### Artifacts
- **Debug APK:** Available for 30 days
- **Release APK:** Available for 90 days (only on main branch)

### Manual Build Trigger
1. Go to GitHub Actions tab
2. Select "Build Android APK" workflow
3. Click "Run workflow"
4. Select environment and run

## 📱 Testing the App

### On Physical Device

1. **Enable Developer Options:**
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times

2. **Enable USB Debugging:**
   - Go to Settings > Developer Options
   - Enable "USB Debugging"

3. **Connect device and run:**
   ```bash
   npm run android:dev
   # In Android Studio, select your device and click Run
   ```

### On Android Emulator

1. **Install Android Studio**
2. **Create an AVD (Android Virtual Device)**
3. **Run:**
   ```bash
   npm run android:dev
   # Select emulator in Android Studio and click Run
   ```

### Testing Backend Connection

1. **Start backend locally:**
   ```bash
   cd ../backend
   python manage.py runserver 0.0.0.0:8000
   ```

2. **Update .env with your local IP:**
   ```env
   VITE_API_URL=http://YOUR_LOCAL_IP:8000
   ```

3. **Rebuild and sync:**
   ```bash
   npm run android:build
   ```

## 🐛 Troubleshooting

### "Network Error" or "Failed to connect"

**Check:**
1. Backend is running on `0.0.0.0:8000`
2. Your device is on the same WiFi network
3. `.env` has correct IP address
4. Test backend in phone browser: `http://YOUR_IP:8000/api/info/`
5. Firewall allows connections on port 8000

**Fix:**
```bash
# Update .env with correct IP
# Rebuild
npm run android:build
```

### "Cleartext HTTP traffic not permitted"

The `network_security_config.xml` should already allow HTTP for local development. If you still see this error:

1. Check `AndroidManifest.xml` has:
   ```xml
   android:networkSecurityConfig="@xml/network_security_config"
   android:usesCleartextTraffic="true"
   ```

2. Verify your IP is in `network_security_config.xml`

3. Rebuild:
   ```bash
   npm run android:build
   ```

### Gradle build errors

```bash
cd android
./gradlew clean
cd ..
npm run cap:sync
```

## 📦 Production Build

### Signing the APK

1. **Generate keystore:**
   ```bash
   keytool -genkey -v -keystore tars-release-key.keystore -alias tars -keyalg RSA -keysize 2048 -validity 10000
   ```

2. **Update `android/app/build.gradle`:**
   ```gradle
   android {
       signingConfigs {
           release {
               storeFile file('path/to/tars-release-key.keystore')
               storePassword 'your-store-password'
               keyAlias 'tars'
               keyPassword 'your-key-password'
           }
       }
       buildTypes {
           release {
               signingConfig signingConfigs.release
           }
       }
   }
   ```

3. **Build release APK:**
   ```bash
   cd android
   ./gradlew assembleRelease
   ```

APK will be in: `android/app/build/outputs/apk/release/`

## 🔐 GitHub Secrets (for CI/CD)

For automatic signing in GitHub Actions, add these secrets:

- `KEYSTORE_PASSWORD` - Keystore password
- `KEY_ALIAS` - Key alias (e.g., "tars")
- `KEY_PASSWORD` - Key password

## 📚 Additional Resources

- [Capacitor Documentation](https://capacitorjs.com/docs)
- [Android Developer Guide](https://developer.android.com/guide)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

## 🆘 Need Help?

See the main project documentation:
- [MOBILE_CONNECTION_GUIDE.md](../MOBILE_CONNECTION_GUIDE.md)
- [CONNECTION_SETUP_COMPLETE.md](../CONNECTION_SETUP_COMPLETE.md)
