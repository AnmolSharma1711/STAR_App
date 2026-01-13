# Update App Icon Script
# Run this after placing your new icon.png in frontend/app/resources/

Write-Host "🎨 Updating STAR App Icon..." -ForegroundColor Cyan

# Step 1: Copy icon from frontend to android-app
$sourcePath = "d:\back\TARS\frontend\app\resources\icon.png"
$destPath = "d:\back\TARS\android-app\resources\icon-foreground.png"

if (Test-Path $sourcePath) {
    Write-Host "✅ Found icon at: $sourcePath" -ForegroundColor Green
    Copy-Item $sourcePath $destPath -Force
    Write-Host "✅ Copied icon to android-app/resources/" -ForegroundColor Green
    
    # Step 2: Generate platform-specific icons
    Write-Host "`n📱 Generating platform-specific icons..." -ForegroundColor Cyan
    Set-Location "d:\back\TARS\android-app"
    
    # Check if capacitor-assets is installed
    $assetsInstalled = npm list -g @capacitor/assets 2>$null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "📦 Installing @capacitor/assets..." -ForegroundColor Yellow
        npm install -g @capacitor/assets
    }
    
    # Generate icons
    npx @capacitor/assets generate --android
    
    Write-Host "`n✅ Icon updated successfully!" -ForegroundColor Green
    Write-Host "`n📝 Next steps:" -ForegroundColor Yellow
    Write-Host "   1. Commit changes: git add . && git commit -m 'Update app icon'" -ForegroundColor Gray
    Write-Host "   2. Push to GitHub: git push star main" -ForegroundColor Gray
    Write-Host "   3. Wait for new APK build on GitHub Actions" -ForegroundColor Gray
    
} else {
    Write-Host "❌ Icon not found at: $sourcePath" -ForegroundColor Red
    Write-Host "`nℹ️  Please:" -ForegroundColor Yellow
    Write-Host "   1. Save your STAR logo as 'icon.png' (1024x1024 PNG)" -ForegroundColor Gray
    Write-Host "   2. Place it at: frontend/app/resources/icon.png" -ForegroundColor Gray
    Write-Host "   3. Run this script again" -ForegroundColor Gray
}
