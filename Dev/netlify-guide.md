# 🚀 Complete Netlify Guide: Deployment and Features

## 📋 Table of Contents
1. [Getting Started](#getting-started)
2. [Deployment Methods](#deployment-methods)
3. [Configuration](#configuration)
4. [Custom Domains](#custom-domains)
5. [Forms](#forms)
6. [Functions](#functions)
7. [Identity](#identity)
8. [Edge Functions](#edge-functions)
9. [Analytics](#analytics)
10. [CLI Reference](#cli-reference)

## 🎯 Getting Started

### Installation
```bash
# Install Netlify CLI
npm install netlify-cli -g

# Login to Netlify
netlify login

# Initialize a new site
netlify init
```

### Quick Deploy
```bash
# Deploy from current directory
netlify deploy

# Deploy to production
netlify deploy --prod

# Deploy with specific build directory
netlify deploy --dir=build --prod
```

## 🔄 Deployment Methods

### Git-Based Deployment
```bash
# Connect to GitHub
netlify init

# Configure build settings in netlify.toml
[build]
  command = "npm run build"
  publish = "build"
  functions = "netlify/functions"
```

### Manual Deployment
```bash
# Deploy specific directory
netlify deploy --dir=public

# Deploy with draft URL
netlify deploy --dir=public --message="Test deployment"

# Deploy to production
netlify deploy --dir=public --prod
```

### Continuous Deployment
```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "dist"

[context.production]
  environment = { NODE_VERSION = "16" }

[context.deploy-preview]
  command = "npm run build:preview"
```

## ⚙️ Configuration

### Basic Configuration
```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "build"
  functions = "netlify/functions"

[dev]
  command = "npm run dev"
  port = 8888
  targetPort = 3000

[context.production.environment]
  REACT_APP_API_URL = "https://api.production.com"

[context.deploy-preview.environment]
  REACT_APP_API_URL = "https://api.staging.com"
```

### Environment Variables
```bash
# Set environment variable
netlify env:set API_KEY "your-api-key"

# List environment variables
netlify env:list

# Import from .env file
netlify env:import .env

# Set for specific context
netlify env:set API_KEY "key" --context production
```

### Build Hooks
```bash
# Create build hook
netlify sites:create-build-hook

# Trigger build
curl -X POST -d {} https://api.netlify.com/build_hooks/<hook_id>
```

## 🌐 Custom Domains

### Domain Management
```bash
# Add custom domain
netlify domains:add example.com

# List domains
netlify domains:list

# Enable HTTPS
netlify sites:enable-https

# Configure DNS
netlify dns:list
netlify dns:add example.com @ A
```

### SSL Configuration
```toml
# Force HTTPS
[[redirects]]
  from = "http://*"
  to = "https://:splat"
  status = 301
  force = true
```

## 📝 Forms

### HTML Form Setup
```html
<!-- Static form -->
<form name="contact" netlify>
  <input type="text" name="name" />
  <input type="email" name="email" />
  <button type="submit">Send</button>
</form>

<!-- Form with file upload -->
<form name="upload" netlify enctype="multipart/form-data">
  <input type="file" name="attachment" />
  <button type="submit">Upload</button>
</form>
```

### JavaScript Form Handling
```javascript
// React form example
const ContactForm = () => {
  const handleSubmit = (e) => {
    e.preventDefault();
    const form = e.target;
    fetch('/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams(new FormData(form)).toString(),
    })
      .then(() => alert('Form submitted'))
      .catch((error) => alert(error));
  };

  return (
    <form
      name="contact"
      method="POST"
      data-netlify="true"
      onSubmit={handleSubmit}
    >
      <input type="hidden" name="form-name" value="contact" />
      <input type="text" name="name" />
      <input type="email" name="email" />
      <button type="submit">Send</button>
    </form>
  );
};
```

## ⚡ Functions

### Function Setup
```javascript
// netlify/functions/hello.js
exports.handler = async (event, context) => {
  return {
    statusCode: 200,
    body: JSON.stringify({ message: 'Hello World' }),
  };
};

// TypeScript function
// netlify/functions/hello.ts
import { Handler } from '@netlify/functions';

export const handler: Handler = async (event, context) => {
  return {
    statusCode: 200,
    body: JSON.stringify({ message: 'Hello World' }),
  };
};
```

### Function Configuration
```toml
# netlify.toml
[functions]
  directory = "netlify/functions"
  node_bundler = "esbuild"

# Function with specific settings
[functions."api/*"]
  included_files = ["data/*.json"]
```

### Scheduled Functions
```javascript
// netlify/functions/cron.js
exports.handler = async (event, context) => {
  // Runs on schedule defined in netlify.toml
};

// netlify.toml
[functions."cron"]
  schedule = "0 5 * * *"
```

## 🔐 Identity

### Setup Identity
```javascript
// Initialize Identity
import GoTrue from 'gotrue-js';

const auth = new GoTrue({
  APIUrl: 'https://your-site.netlify.app/.netlify/identity',
  audience: '',
  setCookie: false,
});
```

### User Management
```javascript
// Sign up
auth.signup(email, password)
  .then(response => console.log("Confirmation email sent"))
  .catch(error => console.log("Error", error));

// Login
auth.login(email, password)
  .then(response => {
    console.log("Logged in", response);
    const user = response;
  })
  .catch(error => console.log("Error", error));

// Logout
auth.currentUser().logout()
  .then(() => console.log("User logged out"))
  .catch(error => console.log("Error", error));
```

## 🌍 Edge Functions

### Edge Function Setup
```javascript
// netlify/edge-functions/transform.js
export default async (request, context) => {
  const response = await context.next();
  const text = await response.text();
  
  return new Response(text.replace(/old/g, 'new'), response);
};
```

### Edge Function Configuration
```toml
# netlify.toml
[[edge_functions]]
  path = "/api/*"
  function = "transform"
```

## 📊 Analytics

### Enable Analytics
```toml
# netlify.toml
[build.processing]
  skip_processing = false
```

### Custom Events
```javascript
// Track custom event
window.netlifyIdentity.on('login', user => {
  window.netlifyAnalytics.track('User Login', {
    userId: user.id,
  });
});
```

## 🛠️ CLI Reference

### Common Commands
```bash
# Site commands
netlify sites:create
netlify sites:list
netlify sites:info

# Deployment
netlify deploy
netlify deploy --prod
netlify deploy --dir=public

# Functions
netlify functions:create
netlify functions:list
netlify functions:serve

# Forms
netlify forms:list
netlify forms:submissions

# Environment
netlify env:list
netlify env:set KEY VALUE
netlify env:import

# Addons
netlify addons:create
netlify addons:list
netlify addons:config

# Development
netlify dev
netlify dev --live
netlify link
```

## 🔍 Debugging

### Logs and Troubleshooting
```bash
# View deploy logs
netlify deploy --debug

# Function logs
netlify functions:logs

# List build settings
netlify build --dry
```

### Common Issues
1. Build Failures
```bash
# Clear cache
netlify deploy --clear

# Force deploy
netlify deploy --force
```

2. Function Timeouts
```toml
# netlify.toml
[functions]
  timeout = 30
```

## 📝 Best Practices

1. **Build Process**
   - Use lock files (package-lock.json, yarn.lock)
   - Set appropriate Node version
   - Optimize build caching

2. **Functions**
   - Keep functions small and focused
   - Use appropriate timeouts
   - Implement proper error handling

3. **Deployment**
   - Use staging environments
   - Implement proper branch workflows
   - Monitor deploy previews

4. **Performance**
   - Enable asset optimization
   - Use appropriate caching headers
   - Implement proper redirects

5. **Security**
   - Secure environment variables
   - Implement proper authentication
   - Use HTTPS only

Remember to:
1. Keep dependencies updated
2. Monitor site performance
3. Review deploy logs regularly
4. Test thoroughly before production deployment
5. Follow security best practices
6. Implement proper error handling
7. Document your configuration