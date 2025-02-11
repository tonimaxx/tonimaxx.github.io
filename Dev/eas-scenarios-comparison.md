# EAS Build Scenarios - Detailed Comparison Guide

## 1. Fresh Project Setup

### Prerequisites
- Node.js installed
- Expo CLI installed
- EAS CLI installed
- Apple/Google developer accounts

### Steps
1. Create Project
```bash
npx create-expo-app MyNewApp
cd MyNewApp
```

2. Initial Setup
```bash
# Install dev client
npx expo install expo-dev-client

# Login to EAS
eas login

# Configure EAS
eas build:configure
```

3. Configure app.json
```json
{
  "expo": {
    "developmentClient": {
      "silentLaunch": true
    }
  }
}
```

4. Set up eas.json (all profiles)
```json
{
  "cli": {
    "version": ">= 5.9.1",
    "appVersionSource": "remote"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal"
    },
    "production": {
      "distribution": "store"
    }
  }
}
```

5. Device Registration (iOS)
```bash
eas device:create
```

6. First Builds
```bash
eas build --profile development --platform ios
eas build --profile development --platform android
```

## 2. Existing Project with EAS ID

### Prerequisites
- Access to existing project repository
- EAS project ID
- Existing credentials

### Steps
1. Clone/Setup Project
```bash
git clone <project-url>
npm install
```

2. Update Dependencies
```bash
npx expo install expo-dev-client
```

3. Link to Existing EAS Project
```bash
eas init --id existing-project-id
```

4. Register New Devices (iOS)
```bash
eas device:create
```

5. Continue with Builds
```bash
eas build --profile development --platform ios
```

## 3. Template-Based Project (TET)

### Prerequisites
- Access to template repository
- Clean template without EAS configuration

### Steps
1. Copy Template
```bash
cp -r TET-Template MyNewProject
cd MyNewProject
```

2. Clean Template-Specific Files
```bash
rm -rf .git
rm -rf node_modules
```

3. Initialize New Project
```bash
npm install
eas init
```

4. Update Configurations
- Update app.json with new project details
- Create new eas.json
- Configure development client

5. Setup and Build
```bash
eas build:configure
eas device:create
eas build --profile development --platform ios
```

## 4. Project Clone/Fork (Project One → Project Two)

### Prerequisites
- Complete Project One with working EAS setup
- Same developer accounts access

### Steps
1. Copy Project
```bash
cp -r ProjectOne ProjectTwo
cd ProjectTwo
```

2. Clean Project-Specific Files
```bash
rm -rf .expo
rm -rf ios
rm -rf android
```

3. Initialize New EAS Project
```bash
eas init
```

4. Update Configurations
```json
// app.json
{
  "expo": {
    "name": "Project Two",
    "slug": "project-two",
    "bundleIdentifier": "com.company.projecttwo"
  }
}
```

5. Reuse eas.json (already optimized)
```json
{
  "cli": {
    "version": ">= 5.9.1",
    "appVersionSource": "remote"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": {
        "resourceClass": "m-medium"
      },
      "android": {
        "buildType": "apk"
      }
    },
    "preview": {
      "distribution": "internal"
    },
    "production": {
      "distribution": "store"
    }
  }
}
```

6. Build Process
```bash
eas build --profile development --platform ios
eas build --profile development --platform android
```

## Comparison Table

| Aspect | Fresh Project | Existing Project | Template-Based | Project Clone |
|--------|---------------|------------------|----------------|---------------|
| Initial Setup | Full setup needed | Minimal setup | Moderate setup | Minimal setup |
| EAS Config | Create new | Reuse existing | Create new | Create new |
| Credentials | New setup | Reuse existing | New setup | Reuse existing |
| Dev Client | Fresh install | Verify/Update | Fresh install | Already configured |
| Build Profiles | Create new | Reuse existing | Create new | Reuse existing |
| Dependencies | Fresh install | Update existing | Fresh install | Update existing |

## Key Differences

### Fresh Project vs Others
- Requires complete setup
- No existing configurations
- New credentials needed

### Existing Project
- Fastest to set up
- Minimal configuration needed
- Credentials already set

### Template-Based
- Clean starting point
- Predefined structure
- Needs new EAS setup

### Project Clone
- Reuses proven setup
- Keeps working configurations
- Just needs new project ID

## Best Practices

1. Version Management
```bash
# Always verify versions
npx expo --version
eas --version
```

2. Credential Management
```bash
# Check credentials status
eas credentials
```

3. Build Verification
```bash
# Always test development build first
eas build --profile development --platform ios
```

4. Environment Configuration
```bash
# Verify environment setup
eas build:configure
```

## Common Issues and Solutions

1. Development Client
```bash
# If dev client not working
eas build --profile development --platform ios --clear-cache
```

2. Credentials Issues
```bash
# Reset credentials if needed
eas credentials:clear
```

3. Build Failures
```bash
# Check build logs
eas build:logs
```

4. Device Registration
```bash
# List registered devices
eas device:list
```
