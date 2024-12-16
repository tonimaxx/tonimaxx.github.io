# 🚀 Complete React Development Guide: From Setup to Deployment

## 📋 Table of Contents
1. [Initial Setup](#initial-setup)
2. [Project Structure](#project-structure)
3. [Essential Components](#essential-components)
4. [State Management](#state-management)
5. [Routing](#routing)
6. [API Integration](#api-integration)
7. [Testing](#testing)
8. [Optimization](#optimization)
9. [Deployment](#deployment)
10. [Best Practices](#best-practices)

## 🎯 Initial Setup

### Create React App
```bash
# Create new project
npx create-react-app my-app
cd my-app

# Create with TypeScript
npx create-react-app my-app --template typescript

# Start development server
npm start
```

### Using Vite (Recommended for newer projects)
```bash
# Create new project
npm create vite@latest my-app -- --template react
cd my-app

# Install dependencies
npm install

# Start development server
npm run dev
```

### Essential Dependencies
```bash
# Routing
npm install react-router-dom

# State Management
npm install @reduxjs/toolkit react-redux

# Styling
npm install tailwindcss postcss autoprefixer
npm install styled-components

# API Calls
npm install axios

# Form Handling
npm install react-hook-form yup @hookform/resolvers

# Testing
npm install @testing-library/react @testing-library/jest-dom

# UI Components
npm install @headlessui/react @heroicons/react
```

## 📁 Project Structure
```plaintext
my-app/
├── public/
│   ├── index.html
│   └── assets/
├── src/
│   ├── components/
│   │   ├── common/
│   │   └── features/
│   ├── pages/
│   ├── hooks/
│   ├── services/
│   ├── utils/
│   ├── store/
│   ├── types/
│   ├── assets/
│   ├── styles/
│   ├── App.tsx
│   └── main.tsx
├── tests/
├── .env
├── package.json
└── vite.config.ts
```

## 🧱 Essential Components

### Functional Component Template
```jsx
import React from 'react';

interface Props {
  title: string;
  children: React.ReactNode;
}

const Component: React.FC<Props> = ({ title, children }) => {
  return (
    <div>
      <h1>{title}</h1>
      {children}
    </div>
  );
};

export default Component;
```

### Custom Hook Example
```jsx
import { useState, useEffect } from 'react';

const useLocalStorage = <T>(key: string, initialValue: T) => {
  const [value, setValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      return initialValue;
    }
  });

  useEffect(() => {
    window.localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
};

export default useLocalStorage;
```

### Context Setup
```jsx
// UserContext.tsx
import React, { createContext, useContext, useState } from 'react';

interface User {
  id: string;
  name: string;
}

interface UserContextType {
  user: User | null;
  setUser: (user: User | null) => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  return (
    <UserContext.Provider value={{ user, setUser }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};
```

## 🔄 State Management

### Redux Setup
```tsx
// store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import userReducer from './userSlice';

export const store = configureStore({
  reducer: {
    user: userReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// store/userSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface UserState {
  user: User | null;
  isLoading: boolean;
}

const initialState: UserState = {
  user: null,
  isLoading: false,
};

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUser: (state, action: PayloadAction<User>) => {
      state.user = action.payload;
    },
    clearUser: (state) => {
      state.user = null;
    },
  },
});

export const { setUser, clearUser } = userSlice.actions;
export default userSlice.reducer;
```

### Using Redux in Components
```tsx
import { useSelector, useDispatch } from 'react-redux';
import { setUser } from '../store/userSlice';
import type { RootState } from '../store';

const UserProfile = () => {
  const dispatch = useDispatch();
  const user = useSelector((state: RootState) => state.user.user);

  const handleLogin = (userData: User) => {
    dispatch(setUser(userData));
  };

  return (
    // Component JSX
  );
};
```

## 🛣️ Routing

### Router Setup
```tsx
// App.tsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ProtectedRoute } from './components/ProtectedRoute';
import { Layout } from './components/Layout';
import { Home, About, Dashboard, NotFound } from './pages';

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route
            path="/dashboard/*"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};
```

### Protected Route Component
```tsx
// components/ProtectedRoute.tsx
import { Navigate, useLocation } from 'react-router-dom';
import { useUser } from '../hooks/useUser';

export const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user } = useUser();
  const location = useLocation();

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
};
```

## 🌐 API Integration

### API Service Setup
```tsx
// services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized
    }
    return Promise.reject(error);
  }
);

export default api;
```

### Custom API Hook
```tsx
// hooks/useApi.ts
import { useState } from 'react';
import api from '../services/api';

export const useApi = <T>() => {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const [loading, setLoading] = useState(false);

  const request = async (
    method: string,
    url: string,
    body?: unknown
  ): Promise<T | null> => {
    try {
      setLoading(true);
      const response = await api.request({
        method,
        url,
        data: body,
      });
      setData(response.data);
      return response.data;
    } catch (err) {
      setError(err as Error);
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { data, error, loading, request };
};
```

## 🧪 Testing

### Component Test Example
```tsx
// components/__tests__/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react';
import { Button } from '../Button';

describe('Button', () => {
  it('renders with correct text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('calls onClick when clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click me</Button>);
    fireEvent.click(screen.getByText('Click me'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });
});
```

### Hook Test Example
```tsx
// hooks/__tests__/useCounter.test.tsx
import { renderHook, act } from '@testing-library/react-hooks';
import { useCounter } from '../useCounter';

describe('useCounter', () => {
  it('should increment counter', () => {
    const { result } = renderHook(() => useCounter());

    act(() => {
      result.current.increment();
    });

    expect(result.current.count).toBe(1);
  });
});
```

## ⚡ Optimization

### React.memo Usage
```tsx
import React from 'react';

interface Props {
  title: string;
  onClick: () => void;
}

const ExpensiveComponent = React.memo<Props>(({ title, onClick }) => {
  return (
    <div onClick={onClick}>
      <h1>{title}</h1>
    </div>
  );
});

export default ExpensiveComponent;
```

### Code Splitting
```tsx
import React, { Suspense } from 'react';

const LazyComponent = React.lazy(() => import('./LazyComponent'));

const App = () => {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <LazyComponent />
    </Suspense>
  );
};
```

## 🚀 Deployment

### Build Project
```bash
# Create production build
npm run build

# Preview production build locally
npm run preview
```

### Deploy to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Deploy to production
vercel --prod
```

### Deploy to Netlify
```bash
# Install Netlify CLI
npm install netlify-cli -g

# Deploy
netlify deploy

# Deploy to production
netlify deploy --prod
```

### Environment Variables
```plaintext
# .env.local
VITE_API_URL=http://localhost:3000
VITE_APP_NAME=My App

# .env.production
VITE_API_URL=https://api.myapp.com
VITE_APP_NAME=My App Production
```

## 💡 Best Practices

### 1. Component Organization
- Keep components small and focused
- Use TypeScript for better type safety
- Implement proper prop validation
- Use meaningful component and file names

### 2. State Management
- Use local state for component-specific data
- Implement Redux for global state
- Use Context for shared state between related components
- Keep state normalized

### 3. Performance
- Implement proper memoization
- Use lazy loading for routes and heavy components
- Optimize images and assets
- Implement proper error boundaries

### 4. Security
- Sanitize user inputs
- Implement proper authentication
- Use HTTPS
- Keep dependencies updated

### 5. Code Quality
- Write meaningful tests
- Use ESLint and Prettier
- Follow consistent coding style
- Document complex logic

### 6. Accessibility
- Use semantic HTML
- Implement proper ARIA labels
- Ensure keyboard navigation
- Test with screen readers

### 7. SEO
- Implement proper meta tags
- Use React Helmet for dynamic head management
- Implement proper routing
- Use SSR when needed

## 📝 Common Gotchas and Solutions

### 1. State Updates
```tsx
// Wrong
setState(state + 1);

// Right
setState(prevState => prevState + 1);
```

### 2. Effect Dependencies
```tsx
// Wrong
useEffect(() => {
  // Effect
}, []); // Missing dependencies

// Right
useEffect(() => {
  // Effect
}, [dependency1, dependency2]);
```

### 3. Event Handlers
```tsx
// Wrong
<button onClick={() => handleClick(id)}>

// Right
const handleClick = useCallback((id: string) => {
  // Handler logic
}, []);
```

Remember to:
1. Keep your dependencies updated
2. Follow React's best practices
3. Write clean, maintainable code
4. Test thoroughly before deployment
5. Monitor your application's performance
6. Keep security in mind
7. Document your code properly