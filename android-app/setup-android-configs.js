const fs = require('fs');
const path = require('path');

console.log('🔧 Setting up Android configurations...\n');

// Check if android folder exists
const androidPath = path.join(__dirname, 'android');
if (!fs.existsSync(androidPath)) {
    console.log('❌ Android platform not added yet. Run: npx cap add android');
    process.exit(1);
}

// Copy network security config
const networkSecuritySource = path.join(__dirname, 'android', 'app', 'src', 'main', 'res', 'xml', 'network_security_config.xml');
const networkSecurityTarget = path.join(androidPath, 'app', 'src', 'main', 'res', 'xml', 'network_security_config.xml');

// Create xml directory if it doesn't exist
const xmlDir = path.dirname(networkSecurityTarget);
if (!fs.existsSync(xmlDir)) {
    fs.mkdirSync(xmlDir, { recursive: true });
}

// Copy AndroidManifest.xml
const manifestSource = path.join(__dirname, 'android', 'app', 'src', 'main', 'AndroidManifest.xml');
const manifestTarget = path.join(androidPath, 'app', 'src', 'main', 'AndroidManifest.xml');

try {
    if (fs.existsSync(networkSecuritySource)) {
        fs.copyFileSync(networkSecuritySource, networkSecurityTarget);
        console.log('✅ Network security config copied');
    }
    
    if (fs.existsSync(manifestSource)) {
        fs.copyFileSync(manifestSource, manifestTarget);
        console.log('✅ AndroidManifest.xml updated');
    }
    
    console.log('\n✅ Android configuration complete!');
    console.log('\nNext steps:');
    console.log('1. npm run build:android');
    console.log('2. npm run cap:sync');
    console.log('3. npm run cap:open\n');
} catch (error) {
    console.error('❌ Error setting up configs:', error.message);
    process.exit(1);
}
