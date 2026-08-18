# FXJ Suits — Next.js + Django

FXJ Suits is a law-firm operations workspace for managing court cases, transactions, legal letters, clients, invoices, expenses, requisitions, land titles, tasks, performance reports, and role-specific dashboards.

The repository is now organized as a single full-stack project. The frontend is a Next.js app under `/frontend`, while the backend is a Django REST API under `/backend`. The core screens and role-aware workflows from the previous Vite/Supabase application have been retained under `frontend/src/legacy-pages` and are mounted through the Next.js app router while their data boundary is migrated to Django.

## Architecture

| Layer | Location | Responsibility |
|---|---|---|
| Next.js frontend | `/frontend` | App-router shell, client-side navigation, responsive dashboard UI, legacy workflow screens, browser-side API client |
| Django backend | `/backend` | REST endpoints, user authentication, role data, record persistence, document uploads, notification relay hooks |
| Local database | `/backend/db.sqlite3` | Development persistence created by Django migrations |
| Uploaded files | `/backend/media` | Development file storage served by Django when `DEBUG=1` |

The API uses a compatibility client in `frontend/src/lib/apiClient.ts`. It preserves the existing context method shape so the screens can move from the old Supabase calls to Django incrementally without rewriting every domain page at once. Browser code no longer contains Supabase service credentials, Telegram bot credentials, or email-provider credentials.

## Local development

Install both application layers from the repository root:

```bash
npm run install:all
```

Create and seed the development database:

```bash
npm run backend:migrate
npm run backend:seed
```

Start the backend in one terminal:

```bash
npm run dev:backend
```

Start the frontend in a second terminal:

```bash
npm run dev:frontend
```

Open [http://localhost:3000](http://localhost:3000). The frontend proxies `/api/backend/*` to Django at `http://127.0.0.1:8000` by default. Set `frontend/.env.local` from `frontend/.env.example` only when the backend is hosted elsewhere.

## Demo account

The seed command creates the following local development account:

| Email | Password | Role |
|---|---|---|
| `admin@buwembo.com` | `password123` | Administrator |

Change this password before using the application with real data. Passwords are hashed by Django; they are no longer stored in browser local storage or queried directly from the frontend.

## Verification commands

Run the frontend production build:

```bash
npm run build
```

Run the Django checks:

```bash
npm run backend:check
```

The staged migration currently keeps a separate `npm run typecheck` command for ongoing legacy-page cleanup. The production Next.js build skips type validation while the preserved screens are being converted; the build and lint pipeline remain active.

## Environment configuration

Backend variables belong in `backend/.env` and should never be exposed through `NEXT_PUBLIC_*` variables. The useful local defaults are:

```dotenv
DJANGO_SECRET_KEY=replace-this-in-production
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
DJANGO_TIME_ZONE=Africa/Kampala
```

Optional email, Telegram, push, and production database settings can be added to Django later. The notification endpoints already terminate in Django so those provider credentials can be integrated without returning secrets to the browser.

## Migration notes

The original Vite entry point, Supabase client, PWA files, and historical scratch scripts remain in the repository history for reference. The active frontend no longer imports the original Supabase browser client. Core record tables are represented by Django’s `GenericRecord` model during the migration so the existing domain JSON can be persisted without losing fields while each domain area is gradually promoted to a typed Django model.

For production, configure PostgreSQL, object storage, HTTPS, secure cookie/token policies, a real email/push provider, and role-based API permissions before connecting the system to real client or case data.
