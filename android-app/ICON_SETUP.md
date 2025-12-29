# Icon Generation Instructions

The TARS logo image has been provided. To use it as the app icon, follow these steps:

## 1. Prepare the Logo

1. Save the provided TARS logo image to: `android-app/icon-source.png`
2. The image should be high resolution (at least 1024x1024px) for best results

## 2. Generate Android Icons

### Option A: Use Online Tool (Easiest)
1. Go to: https://icon.kitchen/ or https://romannurik.github.io/AndroidAssetStudio/
2. Upload the TARS logo
3. Select "Launcher Icons"
4. Download the generated zip file
5. Extract and copy the `res` folder contents to: `android-app/android/app/src/main/res/`

### Option B: Use Capacitor Assets (Recommended)
```bash
cd android-app

# Install capacitor assets plugin
npm install @capacitor/assets --save-dev

# Create resources folder
mkdir -p resources

# Copy your logo to resources/icon.png (must be 1024x1024px)
# The file MUST be named icon.png

# Generate all icons
npx capacitor-assets generate --android
```

This will automatically generate all required icon sizes for Android:
- mipmap-mdpi (48x48)
- mipmap-hdpi (72x72)
- mipmap-xhdpi (96x96)
- mipmap-xxhdpi (144x144)
- mipmap-xxxhdpi (192x192)

## 3. Manual Generation (if needed)

If you need to manually create icons, generate these sizes:

```
res/mipmap-mdpi/ic_launcher.png (48x48)
res/mipmap-hdpi/ic_launcher.png (72x72)
res/mipmap-xhdpi/ic_launcher.png (96x96)
res/mipmap-xxhdpi/ic_launcher.png (144x144)
res/mipmap-xxxhdpi/ic_launcher.png (192x192)

# Rounded versions
res/mipmap-mdpi/ic_launcher_round.png (48x48)
res/mipmap-hdpi/ic_launcher_round.png (72x72)
res/mipmap-xhdpi/ic_launcher_round.png (96x96)
res/mipmap-xxhdpi/ic_launcher_round.png (144x144)
res/mipmap-xxxhdpi/ic_launcher_round.png (192x192)

# Foreground (adaptive icons)
res/mipmap-mdpi/ic_launcher_foreground.png (108x108)
res/mipmap-hdpi/ic_launcher_foreground.png (162x162)
res/mipmap-xhdpi/ic_launcher_foreground.png (216x216)
res/mipmap-xxhdpi/ic_launcher_foreground.png (324x324)
res/mipmap-xxxhdpi/ic_launcher_foreground.png (432x432)
```

## 4. Verify Icon Setup

After generating icons, verify in AndroidManifest.xml:

```xml
<application
    android:icon="@mipmap/ic_launcher"
    android:roundIcon="@mipmap/ic_launcher_round"
    ...>
```

## 5. Rebuild App

```bash
npm run android:build
```

## Quick Script (After placing icon.png in resources/)

```bash
# Create resources directory
mkdir -p android-app/resources

# Place your 1024x1024 TARS logo as: android-app/resources/icon.png

# Install and generate
cd android-app
npm install @capacitor/assets --save-dev
npx capacitor-assets generate --android

# Build app
npm run android:build
```

## Notes

- The icon should have a transparent background for best results
- Android uses adaptive icons, so avoid putting important content near edges
- Test the icon on different Android versions and launchers
- The logo will be automatically resized and optimized
