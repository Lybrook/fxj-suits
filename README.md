# FXJ Suits — Next.js + Django

FXJ Suits is a law-firm operations workspace for court cases, transactions, legal letters, clients, invoices, expenses, requisitions, land titles, tasks, performance reports, and role-specific dashboards.

The repository is a single full-stack project:

| Layer | Location | Responsibility |
|---|---|---|
| Next.js frontend | `/frontend` | App Router shell, responsive interface, role-aware workflows, and browser API client |
| Django backend | `/backend` | REST API, custom token authentication, persistence, uploads, and notification relay hooks |
| Supabase PostgreSQL | External service | Production database used through Django’s `DATABASE_URL` |
| Render | External service | Production Django web service |
| Vercel | External service | Production Next.js frontend |

The active workflow screens are under `frontend/src/legacy-pages`. They are legacy domain screens, not unused files: they are mounted by the Next.js application and use the Django-backed compatibility client in `frontend/src/lib/apiClient.ts`. The file `frontend/src/lib/supabaseClient.ts` is retained as a compatibility export because multiple active screens import that name; it no longer connects to Supabase directly.

## Local development

Install dependencies:

```bash
npm run install:all
```

Create the local database and demo account:

```bash
npm run backend:migrate
npm run backend:seed
```

Run Django in one terminal:

```bash
npm run dev:backend
```

Run Next.js in a second terminal:

```bash
npm run dev:frontend
```

Open [http://localhost:3000](http://localhost:3000). Without a frontend production API variable, Next.js proxies `/api/backend/*` to Django at `http://127.0.0.1:8000`.

The local demo account is:

| Email | Password | Role |
|---|---|---|
| `admin@fxjsuits.co.ke` | `password123` | Administrator |

Change this password before using real data.

## Production deployment

The deployment files are already included:

| File | Purpose |
|---|---|
| `render.yaml` | Render Blueprint for the Django service |
| `backend/build.sh` | Installs Python packages, collects static files, and runs migrations |
| `backend/.env.example` | Server-side Django and Supabase variable template |
| `frontend/.env.example` | Local and Vercel API URL template |
| `VERCEL_RENDER_DJANGO_DEPLOYMENT.md` | Beginner-friendly deployment tutorial |

The intended production flow is:

```text
Vercel Next.js frontend → Render Django API → Supabase PostgreSQL
```

Set this Vercel variable for production:

```text
NEXT_PUBLIC_DJANGO_API_URL=https://your-backend.onrender.com/api
```

Set these Render variables at minimum:

```text
DJANGO_SECRET_KEY=<strong-private-secret>
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=your-backend.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
CSRF_TRUSTED_ORIGINS=https://your-frontend.vercel.app
DATABASE_URL=postgresql://postgres:<encoded-password>@db.<project-ref>.supabase.co:5432/postgres?sslmode=require
DJANGO_TIME_ZONE=Africa/Nairobi
```

Keep `DATABASE_URL`, `DJANGO_SECRET_KEY`, provider credentials, and Supabase service credentials only in Render. Never place them in the Next.js bundle or in a `NEXT_PUBLIC_*` variable.

## Verification commands

Run the Django checks:

```bash
npm run backend:check
```

Run the Next.js production build:

```bash
npm run build
```

Run Django’s production checklist before going live:

```bash
cd backend
python manage.py check --deploy
```

The production service uses Gunicorn through the Render start command:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

Do not use `python manage.py runserver` as the production server.

## Security and data notes

Django hashes passwords on the server. The browser does not store Supabase service credentials or database passwords. The current compatibility layer stores flexible domain records in Django’s `GenericRecord` model so the existing screens can migrate without losing fields. Import old Supabase records only after backing up the project and validating the new Django schema.

For uploaded legal documents, use durable object storage in production rather than relying on a web-service local filesystem. Configure production HTTPS, secure secrets, backups, monitoring, and role-based permissions before using real client or case data.

For the complete Render procedure, open [VERCEL_RENDER_DJANGO_DEPLOYMENT.md](./VERCEL_RENDER_DJANGO_DEPLOYMENT.md).

## References

- [Render — Deploy a Django App](https://render.com/docs/deploy-django)
- [Vercel — Environment Variables](https://vercel.com/docs/environment-variables)
- [Django — Deployment Checklist](https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/)
