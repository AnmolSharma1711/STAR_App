# App Icon Resources

## Icon Requirements

Place your app icon in this directory as:
- **icon.png** - 1024x1024px PNG (Android & iOS)

The icon should:
- Be 1024x1024 pixels
- Have transparent background (or solid color)
- Be in PNG format
- Use high-quality graphics

## Generating Platform Icons

After updating icon.png, run:
```bash
npm install -g @capacitor/assets
npx capacitor-assets generate
```

This will automatically generate all required sizes for Android and iOS.

## Manual Android Update (if needed)

Android icons are located at:
- `android-app/android/app/src/main/res/mipmap-*/ic_launcher.png`

Sizes needed:
- mdpi: 48x48
- hdpi: 72x72  
- xhdpi: 96x96
- xxhdpi: 144x144
- xxxhdpi: 192x192
