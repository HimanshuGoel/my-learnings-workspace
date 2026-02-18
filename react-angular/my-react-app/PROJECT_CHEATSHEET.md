**# Project Cheat Sheet - My React App

---

## 📁 Architecture Overview

### Main Directories and Files

```
my-react-app/
├── public/               # Static assets served as-is
│   └── vite.svg         # Vite logo
├── src/                 # Application source code
│   ├── assets/          # Bundled static assets (images, fonts, etc.)
│   │   └── react.svg    # React logo
│   ├── App.tsx          # Main application component
│   ├── App.css          # App component styles
│   ├── main.tsx         # Application entry point
│   └── index.css        # Global styles
├── index.html           # HTML template entry point
├── package.json         # Project dependencies and scripts
├── tsconfig.json        # TypeScript base configuration
├── tsconfig.app.json    # TypeScript config for app code
├── tsconfig.node.json   # TypeScript config for Node scripts
├── vite.config.ts       # Vite bundler configuration
└── eslint.config.js     # ESLint linting configuration
```

### Key Files Explained

- **[index.html](react-angular/my-react-app/index.html)**: Entry point HTML template; contains `<div id="root">` mount point
- **[src/main.tsx](react-angular/my-react-app/src/main.tsx)**: JavaScript entry point; mounts React app to DOM
- **[src/App.tsx](react-angular/my-react-app/src/App.tsx)**: Root React component
- **[vite.config.ts](react-angular/my-react-app/vite.config.ts)**: Build tool configuration (dev server, build options, plugins)

---

## 🧩 Key Components and Patterns

### Tech Stack

- **React 19.2.0**: Latest React version with improved hooks and performance
- **TypeScript 5.9.3**: Type-safe JavaScript with strict typing
- **Vite 7.2.4**: Fast build tool with HMR (Hot Module Replacement)

### React Patterns Currently in Use

#### 1. **Functional Components**

```tsx
function App() {
  // Component logic
  return <JSX>
}
```

- All components use functional component syntax (no class components)
- Leverages modern React patterns

#### 2. **React Hooks - `useState`**

```tsx
const [count, setCount] = useState(0)
```

- **Location**: [src/App.tsx](react-angular/my-react-app/src/App.tsx#L7)
- Used for local component state management
- Pattern: `const [state, setState] = useState(initialValue)`

#### 3. **StrictMode**

```tsx
<StrictMode>
  <App />
</StrictMode>
```

- **Location**: [src/main.tsx](react-angular/my-react-app/src/main.tsx#L7-L9)
- Enables additional development checks and warnings
- Helps identify potential problems early

#### 4. **Event Handlers (Inline Arrow Functions)**

```tsx
onClick={() => setCount((count) => count + 1)}
```

- Pattern for handling user interactions
- Uses functional state updates for accurate state changes

### Recommended Patterns to Implement

As your app grows, consider implementing:

- **Custom Hooks**: Extract reusable logic (e.g., `useLocalStorage`, `useFetch`)
- **Context API**: For global state management without prop drilling
- **Component Composition**: Break down App.tsx into smaller components
- **React.memo**: For performance optimization of expensive re-renders
- **useEffect**: For side effects (API calls, subscriptions, DOM manipulation)
- **useCallback/useMemo**: For optimizing performance-critical operations

---

## 🔌 APIs and Data Flow

### Current State: **No Backend Integration**

This is a frontend-only application with no API calls yet. Here's how to add backend communication:

### Recommended Approach for API Integration

#### 1. **Fetch API (Native)**

```tsx
useEffect(() => {
  fetch('https://api.example.com/data')
    .then(response => response.json())
    .then(data => setData(data))
    .catch(error => console.error('Error:', error));
}, []);
```

#### 2. **Axios (Recommended - Install First)**

```bash
npm install axios
```

```tsx
import axios from 'axios';

const fetchData = async () => {
  try {
    const response = await axios.get('https://api.example.com/data');
    setData(response.data);
  } catch (error) {
    console.error('Error:', error);
  }
};
```

#### 3. **React Query / TanStack Query (Advanced - Recommended for Complex Apps)**

```bash
npm install @tanstack/react-query
```

```tsx
import { useQuery } from '@tanstack/react-query';

const { data, isLoading, error } = useQuery({
  queryKey: ['todos'],
  queryFn: () => fetch('https://api.example.com/todos').then(res => res.json())
});
```

### Suggested Data Flow Architecture

```
User Interaction (UI Component)
    ↓
Event Handler
    ↓
API Call (useEffect / Custom Hook)
    ↓
Update State (useState / Context / Redux)
    ↓
Re-render Components with New Data
```

### Environment Variables for API URLs

Create `.env` files:

```bash
# .env.development
VITE_API_BASE_URL=http://localhost:3000/api

# .env.production
VITE_API_BASE_URL=https://api.production.com
```

Access in code:
```tsx
const apiUrl = import.meta.env.VITE_API_BASE_URL;
```

---

## 🛠️ Reusable Utilities and Helpers

### Current State: **No Utility Functions Yet**

As the project grows, create a `src/utils/` or `src/lib/` directory for shared functionality.

### Recommended Utility Structure

```
src/
├── utils/
│   ├── api.ts           # API client configuration
│   ├── formatters.ts    # Date, currency, text formatters
│   ├── validators.ts    # Form validation functions
│   └── constants.ts     # App-wide constants
├── hooks/
│   ├── useAuth.ts       # Authentication hook
│   ├── useFetch.ts      # Data fetching hook
│   └── useLocalStorage.ts  # LocalStorage hook
└── helpers/
    ├── storage.ts       # LocalStorage wrapper
    └── debounce.ts      # Performance utilities
```

### Essential Utilities to Create

#### 1. **API Client (`src/utils/api.ts`)**

```tsx
import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Add interceptors for auth tokens
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default apiClient;
```

#### 2. **Custom Fetch Hook (`src/hooks/useFetch.ts`)**

```tsx
import { useState, useEffect } from 'react';

export function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(url);
        const json = await response.json();
        setData(json);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);

  return { data, loading, error };
}
```

#### 3. **LocalStorage Hook (`src/hooks/useLocalStorage.ts`)**

```tsx
import { useState, useEffect } from 'react';

export function useLocalStorage<T>(key: string, initialValue: T) {
  const [value, setValue] = useState<T>(() => {
    const stored = localStorage.getItem(key);
    return stored ? JSON.parse(stored) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue] as const;
}
```

#### 4. **Date Formatter (`src/utils/formatters.ts`)**

```tsx
export const formatDate = (date: Date | string): string => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

export const formatCurrency = (amount: number): string => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD'
  }).format(amount);
};
```

#### 5. **Debounce Utility (`src/utils/debounce.ts`)**

```tsx
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: ReturnType<typeof setTimeout>;
  
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
}
```

### TypeScript Types/Interfaces (`src/types/`)

Create a types directory for shared TypeScript definitions:

```tsx
// src/types/index.ts
export interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

export interface ApiResponse<T> {
  data: T;
  status: number;
  message?: string;
}

export type LoadingState = 'idle' | 'loading' | 'success' | 'error';
```

---

## 🚀 Available Scripts

```bash
npm run dev       # Start development server (http://localhost:5173)
npm run build     # Build for production (outputs to dist/)
npm run preview   # Preview production build locally
npm run lint      # Run ESLint to check code quality
```

---

## 🎯 Quick Development Tips

1. **Hot Module Replacement (HMR)**: Changes to `.tsx` files automatically reload in browser
2. **TypeScript Errors**: Check terminal and VS Code for type errors before running build
3. **Import Aliases**: Currently none configured; consider adding path aliases in `vite.config.ts`
4. **CSS Modules**: Not configured; can add support via Vite config for scoped styles
5. **Testing**: No testing framework installed yet (consider Vitest + React Testing Library)

---

## 📦 Dependencies to Consider Adding

Based on common React app needs:

- **State Management**: `zustand`, `redux-toolkit`, `jotai`
- **Routing**: `react-router-dom`
- **HTTP Client**: `axios`, `@tanstack/react-query`
- **UI Libraries**: `shadcn/ui`, `Material-UI`, `Chakra UI`, `Ant Design`
- **Forms**: `react-hook-form`, `formik`
- **Validation**: `zod`, `yup`
- **Testing**: `vitest`, `@testing-library/react`, `@testing-library/jest-dom`
- **Date Handling**: `date-fns`, `dayjs`
- **Icons**: `lucide-react`, `react-icons`

---

## 🔍 Where to Find Things

| What you need | Where to look |
|---------------|---------------|
| Add new dependencies | `package.json` |
| Configure build | `vite.config.ts` |
| Adjust TypeScript strictness | `tsconfig.json` |
| Add ESLint rules | `eslint.config.js` |
| Create new components | `src/components/` (create this folder) |
| Add API logic | `src/api/` or `src/services/` (create these) |
| Shared utilities | `src/utils/` or `src/lib/` (create these) |
| Custom hooks | `src/hooks/` (create this folder) |
| TypeScript types | `src/types/` (create this folder) |
| Global styles | `src/index.css` |
| Static assets (images, etc.) | `src/assets/` or `public/` |

---

## 🎨 Styling Options

Current: Plain CSS files imported into components

**Options to consider:**

- **CSS Modules**: Scoped styles (built into Vite)
- **Tailwind CSS**: Utility-first CSS framework
- **Styled Components**: CSS-in-JS
- **Sass/SCSS**: CSS preprocessor
- **Emotion**: Another CSS-in-JS library

---

## 🧪 Best Practices Checklist

- [ ] Create a proper folder structure (`components/`, `hooks/`, `utils/`, etc.)
- [ ] Set up path aliases for cleaner imports
- [ ] Add environment variables for configuration
- [ ] Implement error boundaries for graceful error handling
- [ ] Create reusable custom hooks for common logic
- [ ] Add PropTypes or enforce strict TypeScript types
- [ ] Implement code splitting for large components
- [ ] Set up a testing framework
- [ ] Add a linter pre-commit hook (husky + lint-staged)
- [ ] Document component APIs with JSDoc comments
- [ ] Create a storybook for component documentation
- [ ] Set up CI/CD pipeline for automated testing and deployment

---

**Last Updated**: February 12, 2026  
**Project Version**: 0.0.0  
**React Version**: 19.2.0  
