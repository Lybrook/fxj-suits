# Put the Django Backend Online with a Vercel Frontend

## What you are building

Your application will use three separate services:

| Part | Service | Purpose |
|---|---|---|
| Frontend | Vercel | Hosts the Next.js interface |
| Backend | Render Web Service | Runs Django and exposes the REST API |
| Database | Supabase PostgreSQL | Stores users, cases, clients, and other data |

The browser should call **Django**, and Django should call **Supabase**. The browser should never receive the Supabase database password.

> You cannot normally deploy a long-running Django server inside Supabase. Supabase provides the database and related services; a separate Python-capable host such as Render runs Django.

This arrangement follows Render’s Django deployment pattern of using a production server, environment variables, migrations, and a build command.[1] Vercel environment variables are configured per environment and apply to new deployments.[2] Django’s own documentation recommends not using `runserver` in production and running the deployment checklist.[3]

## Before you start

You need the following:

1. A GitHub account with the `Lybrook/fxj-suits` repository.
2. A Supabase project and its PostgreSQL connection string.
3. A Vercel project already connected to the repository.
4. A Render account connected to GitHub.
5. The public URL of the Vercel frontend after it is deployed.

For the examples below, replace these placeholders:

```text
YOUR_FRONTEND_URL=https://your-frontend.vercel.app
YOUR_BACKEND_URL=https://fxj-suits-api.onrender.com
YOUR_SUPABASE_DATABASE_URL=your Supabase PostgreSQL URL
```

Do not include a trailing slash in `YOUR_FRONTEND_URL` or `YOUR_BACKEND_URL`.

## Part 1: Prepare the Django backend

### Step 1: Add production dependencies

Open `backend/requirements.txt` and make sure it includes these packages:

```text
Django>=5.1,<6.0
djangorestframework>=3.15,<4.0
django-cors-headers>=4.6,<5.0
python-dotenv>=1.0,<2.0
dj-database-url>=2.2,<3.0
psycopg[binary]>=3.2,<4.0
gunicorn>=23.0,<24.0
whitenoise[brotli]>=6.8,<7.0
```

The first four are already part of the converted project. The last four are needed for Supabase PostgreSQL, production serving, and static files.

Commit these changes and push them to GitHub:

```bash
git add backend/requirements.txt
git commit -m "Prepare Django backend for production hosting"
git push origin main
```

### Step 2: Configure Django to use Supabase PostgreSQL

Open `backend/config/settings.py`.

At the top, add:

```python
import dj_database_url
```

Replace the current `DATABASES` section with:

```python
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / os.getenv("DJANGO_DB_NAME", "db.sqlite3"),
        }
    }
```

This means local development can still use SQLite, but the online backend uses Supabase whenever `DATABASE_URL` is present.

### Step 3: Update production settings

Change the default production-sensitive values so they come from environment variables:

```python
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = os.getenv("DJANGO_DEBUG", "0") == "1"

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("DJANGO_ALLOWED_HOSTS", "localhost").split(",")
    if host.strip()
]
```

For production, Render will need a real secret key and `DJANGO_DEBUG=0`. Django warns that debug mode must not be enabled in production because it can reveal source code, settings, and sensitive request information.[3]

Keep this REST configuration because the repository uses the custom `UserProfileTokenAuthentication` class:

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "core.authentication.UserProfileTokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}
```

### Step 4: Add WhiteNoise for static files

In `backend/config/settings.py`, add WhiteNoise immediately after Django’s `SecurityMiddleware`:

```python
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # the remaining middleware stays unchanged
]
```

At the static-file section, use:

```python
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

if not DEBUG:
    STORAGES = {
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }
```

WhiteNoise lets the Render web service serve Django’s collected static files without requiring a separate Nginx configuration.[1]

### Step 5: Configure CORS for Vercel

In `backend/config/settings.py`, set CORS from an environment variable:

```python
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
    if origin.strip()
]
CORS_ALLOW_CREDENTIALS = True
```

Do not put a trailing slash in the origin. The correct value is:

```text
https://your-frontend.vercel.app
```

The incorrect value is:

```text
https://your-frontend.vercel.app/
```

### Step 6: Confirm the Django WSGI entry point

The repository already has:

```text
backend/config/wsgi.py
```

Render will run it using Gunicorn. The production start command will be:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

Do not use this in production:

```bash
python manage.py runserver
```

Django explicitly states that `runserver` is not designed for production deployment.[3]

## Part 2: Deploy Django on Render

### Step 7: Create the Render web service

1. Open [Render](https://render.com/) and sign in with GitHub.
2. Click **New**.
3. Select **Web Service**.
4. Select the `Lybrook/fxj-suits` repository.
5. Choose a service name, for example `fxj-suits-api`.
6. Select **Python** as the runtime.
7. Set the **Root Directory** to:

```text
backend
```

Setting the root directory to `backend` means Render will run commands from the Django folder, where `manage.py` and `requirements.txt` are located.

8. Set the **Build Command** to:

```bash
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
```

9. Set the **Start Command** to:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

10. Choose the service plan you want to use.
11. Do not deploy yet until you add the environment variables in the next step.

Render’s official Django guide supports either a dashboard-based setup or a repository `render.yaml` blueprint.[1] The dashboard method is easier for a first deployment.

### Step 8: Add Render environment variables

In the Render service, open **Environment** and add these variables:

| Name | Value |
|---|---|
| `DJANGO_SECRET_KEY` | Generate a long random value using Render’s secret generator if available |
| `DJANGO_DEBUG` | `0` |
| `DJANGO_ALLOWED_HOSTS` | `fxj-suits-api.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | `https://your-frontend.vercel.app` |
| `DATABASE_URL` | Your Supabase PostgreSQL connection string |
| `DJANGO_TIME_ZONE` | `Africa/Nairobi` |

If you have a custom frontend domain, include both origins separated by a comma:

```text
https://your-frontend.vercel.app,https://app.yourdomain.com
```

If your Render URL is different, use the exact hostname Render gives you in `DJANGO_ALLOWED_HOSTS`.

If you use a Supabase password containing characters such as `@`, `#`, `?`, `/`, or `:`, URL-encode the password portion of `DATABASE_URL`. For example, `@` becomes `%40` and `#` becomes `%23`.

### Step 9: Deploy and find the backend URL

Click **Create Web Service**. Render will install dependencies, run the build command, apply migrations to Supabase, collect static files, and start Gunicorn.

When deployment succeeds, Render gives you a URL similar to:

```text
https://fxj-suits-api.onrender.com
```

Test the backend in a browser by opening:

```text
https://fxj-suits-api.onrender.com/health/
```

You should see:

```json
{"status": "ok", "service": "fxj-suits-api"}
```

If the deployment fails, open the Render **Logs** tab and look for the first error, not only the final error message.

## Part 3: Connect Vercel to Django

### Step 10: Set the Vercel API URL

Open your Vercel project:

1. Go to **Settings**.
2. Open **Environment Variables**.
3. Add this variable:

```text
Name: NEXT_PUBLIC_DJANGO_API_URL
Value: https://fxj-suits-api.onrender.com/api
```

Select **Production**. Select **Preview** too if you want preview deployments to use the same backend.

The FXJ Suits frontend builds its API requests as follows:

```text
NEXT_PUBLIC_DJANGO_API_URL + /auth/login
NEXT_PUBLIC_DJANGO_API_URL + /records/clients
```

Therefore the value must end with `/api`, not only the hostname.

Correct:

```text
https://fxj-suits-api.onrender.com/api
```

Incorrect:

```text
https://fxj-suits-api.onrender.com
```

Vercel environment variable changes apply to new deployments, so redeploy the frontend after saving the variable.[2]

### Step 11: Confirm the Vercel project root

Because this repository contains both `/frontend` and `/backend`, the Vercel project should use:

```text
Root Directory: frontend
```

The Vercel build settings should normally be:

```text
Install Command: npm install
Build Command: npm run build
Output: Next.js default
```

If Vercel is currently trying to build from the repository root, change the root directory to `frontend` and redeploy.

### Step 12: Redeploy Vercel

In Vercel, open **Deployments** and click **Redeploy**, or push a new commit to the production branch.

After deployment, open the Vercel URL and try to log in with the seeded administrator account. The browser should call the Render backend URL, not localhost.

## Part 4: Test the complete system

### Test 1: Backend health

Open:

```text
https://fxj-suits-api.onrender.com/health/
```

Expected result:

```json
{"status": "ok", "service": "fxj-suits-api"}
```

### Test 2: Backend login

From a terminal:

```bash
curl -X POST https://fxj-suits-api.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@fxjsuits.co.ke","password":"password123"}'
```

The response should include a token.

### Test 3: Frontend login

Open the Vercel URL, go to the login screen, and use the demo account. If login fails, open the browser developer tools with `F12`, select the **Network** tab, and inspect the request to `/auth/login`.

### Test 4: CORS

If the browser console says something like:

```text
blocked by CORS policy
```

check these values in Render:

```text
CORS_ALLOWED_ORIGINS=https://your-real-vercel-domain.vercel.app
```

Make sure the value exactly matches the address in the browser address bar, including `https://`, and does not have a trailing slash.

### Test 5: Database

Open the Supabase Table Editor and confirm that Django tables exist. If Render logs say that a table does not exist, verify that the build command ran:

```bash
python manage.py migrate
```

## Common problems

| Problem | Likely cause | Fix |
|---|---|---|
| Vercel calls `localhost:8000` | `NEXT_PUBLIC_DJANGO_API_URL` is missing | Add it in Vercel and redeploy |
| Browser reports CORS failure | Vercel URL is missing or has a trailing slash in CORS settings | Set the exact Vercel origin in `CORS_ALLOWED_ORIGINS` |
| Render cannot import `gunicorn` | Gunicorn is missing from `requirements.txt` | Add `gunicorn` and redeploy |
| Render says `No module named config` | Root directory or start command is wrong | Set root directory to `backend`; use `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT` |
| Supabase login fails | Database URL or password is incorrect | Recopy the Supabase connection string and URL-encode special password characters |
| `DisallowedHost` appears | Backend hostname is missing from `DJANGO_ALLOWED_HOSTS` | Add the exact Render hostname and redeploy |
| Database tables are missing | Migrations did not run | Add `python manage.py migrate` to the build command and redeploy |
| Uploaded files disappear | Render local disk is not a permanent file store | Use Supabase Storage or another object-storage provider for production documents |
| Production shows a Django traceback | `DJANGO_DEBUG=1` | Set `DJANGO_DEBUG=0` and redeploy |
| Changes to Vercel variables have no effect | Existing deployment still uses old variables | Create a new deployment after changing variables |

## Production safety checklist

Before sharing the live system with real users:

```bash
python manage.py check --deploy
```

Also confirm the following:

- `DJANGO_DEBUG=0`.
- `DJANGO_SECRET_KEY` is a strong secret and is not committed to GitHub.
- `DATABASE_URL` is stored only in Render, not in Vercel or frontend source code.
- Django is running through Gunicorn, not `runserver`.
- `DJANGO_ALLOWED_HOSTS` contains the Render backend hostname.
- `CORS_ALLOWED_ORIGINS` contains only the real frontend domains.
- HTTPS is enabled for both Vercel and Render.
- Supabase backups are enabled before importing real legal data.
- Production document uploads use durable object storage rather than Render’s local filesystem.
- You have tested login, reading records, creating records, and uploading documents.

## References

[1]: https://render.com/docs/deploy-django "Render: Deploy a Django App"

[2]: https://vercel.com/docs/environment-variables "Vercel: Environment Variables"

[3]: https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/ "Django: Deployment Checklist"
