# GitHub Copilot Instructions

## Project Overview

This is a personal knowledge hub for documenting weekly learnings, including notes from tutorials, research, best practices, and summarized insights across various technology domains.

## Project Structure

This repository contains multiple learning domains:

- **__future__/**: Future learning materials and explorations
- **react-angular/**: React and Angular learnings and practical projects
- **typescript-javascript/**: TypeScript and JavaScript best practices
- **generative-ai/**: GenAI learnings and implementations
- **system-design/**: System design patterns and architectures
- **docker-kubernetes-cloud/**: Container orchestration and cloud technologies
- **soft-skills/**: Professional development and soft skills
- **wellness-philosophy-lifestyle/**: Personal wellbeing and lifestyle
- **tech-gadgets-games-science/**: Technology trends and innovations
- **stumble-upon/**: Miscellaneous discoveries

## Code Style and Conventions

### React/TypeScript Projects

When working with React applications (e.g., [react-angular/my-react-app](react-angular/my-react-app)):

1. **Use Functional Components** - No class components
2. **TypeScript Strict Mode** - Always include proper type annotations
3. **React Hooks** - Prefer hooks (useState, useEffect, useCallback, useMemo)
4. **File Organization**:
   - Components in `src/components/`
   - Custom hooks in `src/hooks/`
   - Utilities in `src/utils/`
   - Types in `src/types/`
   - API logic in `src/api/` or `src/services/`

### Naming Conventions

- **Components**: PascalCase (e.g., `UserProfile.tsx`)
- **Hooks**: camelCase with 'use' prefix (e.g., `useAuth.ts`, `useFetch.ts`)
- **Utilities**: camelCase (e.g., `formatDate.ts`, `api.ts`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `API_BASE_URL`)
- **Types/Interfaces**: PascalCase (e.g., `User`, `ApiResponse<T>`)

### React Patterns to Follow

```tsx
// ✅ Functional components with TypeScript
interface Props {
  title: string;
  count: number;
}

function MyComponent({ title, count }: Props) {
  const [state, setState] = useState<number>(0);
  
  useEffect(() => {
    // Side effects here
  }, []);
  
  return <div>{title}: {count}</div>;
}

// ✅ Custom hooks for reusable logic
function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);
  
  // Hook logic...
  
  return { data, loading, error };
}

// ✅ Functional state updates
onClick={() => setCount((prev) => prev + 1)}
```

## API Integration Guidelines

When adding API calls:

1. **Create an API client** in `src/utils/api.ts` with axios or fetch
2. **Use async/await** for cleaner promise handling
3. **Create custom hooks** for data fetching (e.g., `useFetch`, `useQuery`)
4. **Handle loading and error states** explicitly
5. **Use environment variables** for API URLs (e.g., `VITE_API_BASE_URL`)

Example:
```tsx
// src/utils/api.ts
import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
});

export default apiClient;
```

## Utility Functions

Create reusable utilities in `src/utils/`:

- `formatters.ts` - Date, currency, text formatting
- `validators.ts` - Form validation
- `constants.ts` - App-wide constants
- `debounce.ts` - Performance utilities

## State Management

- **Local state**: `useState` hook
- **Complex state**: Consider `useReducer`
- **Global state**: Context API or external libraries (zustand, redux-toolkit)
- **Server state**: React Query / TanStack Query for API data

## Documentation Standards

### Markdown Files

- Use clear headings (##, ###)
- Include code examples with proper language tags
- Add links to relevant files: `[filename](path/to/file)`
- Include "Last Updated" dates for accuracy

### Code Comments

```tsx
/**
 * Fetches user data from the API
 * @param userId - The unique identifier of the user
 * @returns Promise resolving to User object
 * @throws Error if fetch fails
 */
async function fetchUser(userId: string): Promise<User> {
  // Implementation
}
```

## Testing Approach

When adding tests:

- Use **Vitest** for unit testing
- Use **React Testing Library** for component testing
- Place tests next to source files: `Component.test.tsx`
- Follow AAA pattern: Arrange, Act, Assert

## Styling Guidelines

Current: Plain CSS with component-specific CSS files

Preferred patterns:
- **CSS Modules** for scoped styles
- **Tailwind CSS** for utility-first approach (if adopted)
- Keep global styles minimal in `index.css`

## Dependencies to Consider

Before suggesting new dependencies, check if they fit these categories:

- **State Management**: zustand, redux-toolkit
- **Routing**: react-router-dom
- **HTTP Client**: axios, @tanstack/react-query
- **UI Libraries**: shadcn/ui, Material-UI, Chakra UI
- **Forms**: react-hook-form, zod
- **Testing**: vitest, @testing-library/react
- **Utilities**: date-fns, lodash-es

## Build Tools

- **Vite** for bundling and dev server
- **TypeScript** for type safety
- **ESLint** for code linting
- Scripts: `npm run dev`, `npm run build`, `npm run preview`

## Performance Best Practices

1. Use `React.memo` for expensive components
2. Implement `useCallback` and `useMemo` for optimization
3. Code split large components with `React.lazy`
4. Debounce user inputs for search/filter operations
5. Use virtualization for long lists (react-window, react-virtualized)

## Error Handling

- Create error boundaries for graceful error handling
- Always handle promise rejections
- Provide user-friendly error messages
- Log errors appropriately (console.error in dev, logging service in prod)

## Environment Setup

```bash
# Development
npm run dev

# Production build
npm run build
npm run preview
```

## Reference Documentation

For detailed architecture and patterns, refer to:
- [Project Cheat Sheet](react-angular/my-react-app/PROJECT_CHEATSHEET.md) - Complete React app architecture guide
- Individual `BEST_PRACTICES.md` files in each domain folder
- `README.md` files for domain-specific guidelines

## Commit Message Format

```
<type>: <description>

Examples:
feat: add user authentication hook
fix: resolve state update issue in counter
docs: update API integration guide
refactor: extract reusable form validation logic
style: format code with prettier
test: add tests for useFetch hook
```

## Quick Reference

| Task | Location |
|------|----------|
| Add component | `src/components/` |
| Create custom hook | `src/hooks/` |
| Add utility function | `src/utils/` |
| Define types | `src/types/` |
| API integration | `src/api/` or `src/services/` |
| Global styles | `src/index.css` |
| Static assets | `src/assets/` or `public/` |
| Environment config | `.env.development` / `.env.production` |

---

**Note**: This project emphasizes learning and best practices. When suggesting code, prioritize readability, maintainability, and TypeScript type safety. Always reference the project cheat sheet for architectural decisions.

**Last Updated**: February 12, 2026
