## 📱 Place Your TARS Logo Here

This folder is for your app icon source image.

### Required File:
**`icon.png`** - Your TARS logo (1024x1024px recommended)

### Steps to Add Icon:

1. **Save the TARS logo image** you provided as `icon.png` in this folder
2. **Ensure it's high quality:** 1024x1024px minimum
3. **Run the generator:**
   ```bash
   cd ..
   npm run generate:icons
   ```

### Image Requirements:
- ✅ Format: PNG (recommended)
- ✅ Size: 1024x1024px (or larger)
- ✅ Background: Transparent or solid color
- ✅ Content: Avoid important content near edges (due to adaptive icons)

### After Generating Icons:

The script will create all Android icon sizes in:
```
android/app/src/main/res/mipmap-*/
```

Then rebuild your app:
```bash
npm run android:build
```

### Alternative: Manual Placement

If you already have generated Android icons, you can manually place them in:
```
android/app/src/main/res/mipmap-mdpi/ic_launcher.png
android/app/src/main/res/mipmap-hdpi/ic_launcher.png
android/app/src/main/res/mipmap-xhdpi/ic_launcher.png
android/app/src/main/res/mipmap-xxhdpi/ic_launcher.png
android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png
```

---

**📝 Note:** The TARS logo file from your previous message should be saved here as `icon.png`
