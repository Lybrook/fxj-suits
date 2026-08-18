# FXJ Suits migration audit

## Target architecture

- Single repository with `/frontend` and `/backend` directories.
- Frontend: Next.js + TypeScript.
- Backend: Django + Django REST Framework.
- Core domain behavior should remain available while the visual interface may be redesigned.

## Existing application

The repository is a Vite React/TypeScript law-firm management system. The main application shell is `src/App.tsx`, which currently uses React Router, a role-aware `ProtectedRoute`, a shared admin sidebar layout, an offline banner, update notifications, and role-specific dashboards.

Current route groups include login/reset-password, management dashboards, clients, invoices, reports, expenses, requisitions, transactions, court cases, letters, lawyers, archive, land titles and details, lawyer dashboards and details, clerk dashboard, performance, and court calendar.

The central `src/context/AppContext.tsx` file contains the effective client-side domain contract and currently combines localStorage persistence, Supabase reads/writes, authentication, file uploads, notifications, email/push side effects, offline sync, and CRUD logic. The domain collections are users, transactions, court cases, letters, invoices, clients, communication logs, tasks, draft requests, filing requests, notifications, land titles/notes, expenses, and requisitions.

## Existing integrations to replace or isolate

- Supabase browser client/auth/storage/realtime: `src/lib/supabaseClient.ts`, `src/context/AppContext.tsx`.
- Supabase edge functions for email and push notifications.
- Supabase storage buckets for transaction and letter documents.
- Telegram calls in `src/pages/Requisitions.tsx`.
- Vite `import.meta.env` references in `AppContext.tsx`, `supabaseClient.ts`, and `Requisitions.tsx`.
- Service-worker/PWA files under `public/` and root Vite configuration.

## Migration strategy

1. Preserve the existing page/component code as the initial UI implementation under `/frontend`, then adapt the application shell to Next.js-compatible routing and client boundaries rather than rewriting every business screen immediately.
2. Replace the browser Supabase client with a compatibility data client that talks to Django REST endpoints and keeps the existing context methods stable while the pages are migrated incrementally.
3. Build a Django API with explicit domain models, role-aware authentication, CRUD endpoints, document upload endpoints, and seed data support. Use SQLite by default for local development, with PostgreSQL configuration documented as the production option.
4. Move secrets out of the browser. Email, push, and Telegram behavior should be backend-owned and fail safely when optional credentials are absent.
5. Add clear root-level development commands and environment examples for both services.
