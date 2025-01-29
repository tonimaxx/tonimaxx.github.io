# Complete Guide: Switching from Expo Go to Development Client

## Table of Contents
- [Prerequisites](#prerequisites)
- [Initial Setup](#initial-setup)
- [EAS Configuration](#eas-configuration)
- [Building Development Client](#building-development-client)
- [Device Management](#device-management)
- [Running Your App](#running-your-app)
- [Troubleshooting](#troubleshooting)

## Prerequisites
- Node.js installed
- Expo CLI installed
- EAS CLI installed
- Apple Developer Account (for iOS)
- Xcode installed (for iOS)
- Android Studio (for Android)

## Initial Setup

1. Install required packages:
```bash
# Install expo-dev-client
npx expo install expo-dev-client

# Install EAS CLI if not installed
npm install -g eas-cli

# Login to EAS
eas login
```

2. Configure your app.json/app.config.js:
```json
{
  "expo": {
    "developmentClient": {
      "silentLaunch": true
    }
  }
}
```

## EAS Configuration

1. Initialize EAS configuration:
```bash
eas build:configure
```

2. Create eas.json (or modify existing):
```json
{
  "cli": {
    "version": ">= 5.9.1"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "android": {
        "gradleCommand": ":app:assembleDebug",
        "buildType": "apk"
      },
      "ios": {
        "resourceClass": "m1-medium",
        "simulator": true
      },
      "env": {
        "APP_ENV": "development"
      }
    },
    "preview": {
      "distribution": "internal",
      "android": {
        "buildType": "apk"
      },
      "ios": {
        "resourceClass": "m1-medium"
      }
    },
    "production": {
      "distribution": "store",
      "android": {
        "buildType": "app-bundle"
      },
      "ios": {
        "resourceClass": "m1-medium"
      }
    }
  }
}
```

## Building Development Client

### For iOS

1. Register devices for development:
```bash
# Clear any existing credentials (optional)
eas credentials:clear

# Register devices
eas device:create

# List registered devices
eas device:list
```

2. Build development client:
```bash
# For iOS simulator
eas build --profile development --platform ios

# For physical device
eas build --profile development --platform ios --no-simulator
```

### For Android

1. Build development client:
```bash
eas build --profile development --platform android
```

## Device Management

### iOS Device Registration

1. List current devices:
```bash
eas device:list
```

2. Add new devices:
```bash
eas device:create
```

3. After adding new devices, rebuild:
```bash
eas build --profile development --platform ios --clear-credentials
```

### Android Device Setup
- No registration needed
- APK can be installed on any device

## Running Your App

1. Start the development server:
```bash
npx expo start --dev-client
```

2. Install the app:
- iOS: Use TestFlight or direct installation
- Android: Install APK directly

3. Development options:
- Shake device for dev menu
- Use ⌘D on iOS simulator
- Use cmd+m on Android emulator

## Troubleshooting

### Common iOS Issues

1. "Unable to install" error:
```bash
# Clear credentials and rebuild
eas credentials:clear
eas build --profile development --platform ios --clear-credentials
```

2. Signing issues:
- Verify Apple Developer account
- Check device registration
- Rebuild with cleared credentials

3. Installation fails:
- Delete existing app
- Restart device
- Clear simulator:
```bash
xcrun simctl remove_uninstalled_apps
```

### Common Android Issues

1. APK installation fails:
- Enable developer options
- Allow installation from unknown sources
- Clear previous installations

2. Development client not connecting:
- Check same network
- Try different dev client options
- Rebuild with latest configuration

## Best Practices

1. Development workflow:
- Use development build for daily development
- Use preview build for testing
- Use production build for store submission

2. Version management:
- Keep Expo SDK updated
- Maintain consistent node modules
- Regular rebuilds with latest changes

3. Team development:
- Use preview builds for team testing
- TestFlight for iOS team distribution
- Direct APK sharing for Android

## Commands Quick Reference

```bash
# Development client installation
npx expo install expo-dev-client

# EAS commands
eas login
eas build:configure
eas device:create
eas device:list
eas credentials:clear
eas build --profile development --platform ios
eas build --profile development --platform android

# Running the app
npx expo start --dev-client
```

## Notes
- Always rebuild development client after adding new native dependencies
- Keep track of registered devices for iOS development
- Regular cleanup of old builds and credentials
- Maintain separate environments (dev/staging/prod)
