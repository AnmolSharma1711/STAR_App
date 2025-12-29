import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.tars.app',
  appName: 'TARS',
  webDir: 'dist',
  server: {
    androidScheme: 'https',
    // Allow cleartext traffic for local development
    cleartext: true,
    // Allowed navigation for production API
    allowNavigation: [
      'https://tars-bkv7.onrender.com',
      'http://192.168.198.127:8000',
      'http://192.168.56.1:8000',
      'http://localhost:8000'
    ]
  },
  android: {
    allowMixedContent: true
  }
};

export default config;
