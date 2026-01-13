# Android Network Security Configuration

After running `npx cap add android`, create this file to allow local development connections:

## File: `android/app/src/main/res/xml/network_security_config.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <!-- Allow cleartext (HTTP) traffic for local development -->
    <domain-config cleartextTrafficPermitted="true">
        <!-- Your local network IPs -->
        <domain includeSubdomains="true">192.168.198.127</domain>
        <domain includeSubdomains="true">192.168.56.1</domain>
        <!-- Android emulator localhost -->
        <domain includeSubdomains="true">10.0.2.2</domain>
        <domain includeSubdomains="true">localhost</domain>
    </domain-config>
    
    <!-- Default: Only allow HTTPS -->
    <base-config cleartextTrafficPermitted="false" />
</network-security-config>
```

## Update: `android/app/src/main/AndroidManifest.xml`

Add the `android:networkSecurityConfig` attribute to the `<application>` tag:

```xml
<application
    android:networkSecurityConfig="@xml/network_security_config"
    android:usesCleartextTraffic="true"
    android:allowBackup="true"
    ...>
    <!-- rest of your application config -->
</application>
```

## Internet Permission

Ensure `android/app/src/main/AndroidManifest.xml` has internet permission:

```xml
<manifest ...>
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    ...
</manifest>
```

## Build & Run Commands

```bash
# For local development
npm run build
npx cap sync
npx cap open android

# For production
npm run build --mode production
npx cap sync
npx cap open android
```

## Testing Different Backends

### Local Development (HTTP):
- Edit `.env.android` to use: `VITE_API_URL=http://192.168.198.127:8000`
- Rebuild: `npm run build`
- Sync: `npx cap sync`

### Production (HTTPS):
- Edit `.env.android` to use: `VITE_API_URL=https://tars-bkv7.onrender.com`
- Rebuild: `npm run build --mode production`
- Sync: `npx cap sync`

## Important Notes

1. **Replace IP Addresses**: Update `192.168.198.127` and `192.168.56.1` with YOUR actual local IP addresses
2. **Find Your IP**: Run `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
3. **Backend Must Be Running**: Ensure Django backend is accessible at `http://YOUR_IP:8000`
4. **Test Backend**: From your phone's browser, visit `http://YOUR_IP:8000/api/info/`
5. **Production Builds**: Use HTTPS URLs only (remove cleartext permissions)
