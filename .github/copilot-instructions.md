## Purpose
This file contains concise, codebase-specific guidance for AI coding agents (Copilot-like) to be immediately productive in this Django project.

## Big picture (what this repo is)
- A Django 5.2 monolith with small apps: `pets`, `shelters`, `users`, `newsletter` and utility modules under `project/` and `utils/`.
- Static templates live in `base_templates/` and shared static assets in `base_static/`.
- Two runtime modes for DB/storage: local Docker MySQL (via `DB_LOCAL=True`) or remote Postgres (Supabase) when `DB_LOCAL` is not set. See `project/settings.py`.
- File-storage: local filesystem in development, Backblaze B2 (via `django-storages` AWS interface) in production when `AWS_ACCESS_KEY_ID` is present. The storage backends live under `project/storage_backends.py` (referenced by `STORAGES`).

## Key workflows (how maintainers run & test)
- Tests: run `pytest` — configuration is in `pytest.ini` which sets `DJANGO_SETTINGS_MODULE = project.settings_test` (tests use an SQLite DB and filesystem-backed media/static). See `conftest.py` for fixtures that create temporary `MEDIA_ROOT` and `STATIC_ROOT`.
- Local dev (without Docker): usual `python manage.py runserver` (settings default points to env vars).
- Dockerized dev/prod: `docker-compose.yml` builds the image and runs `wait-for-db.sh` then `gunicorn` via `start.sh`. The Dockerfile installs system deps (MySQL client headers, netcat, etc.). `start.sh` runs migrations and `collectstatic` then starts Gunicorn.

## Important environment variables and switches
- `SECRET_KEY`, `DEBUG` — standard Django
- DB: `DB_LOCAL` (set to 'True' for local MySQL), `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` — `project/settings.py` branches on `DB_LOCAL`.
- Mailer: `MAILERLITE_API_KEY`, `MAILERLITE_NEWSLETTER_GROUP_ID` — newsletter integration.
- Storage (Backblaze B2 via S3 API): `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, `AWS_S3_REGION_NAME` — when present the project uses `project.storage_backends.MediaStorage` and sets `MEDIA_URL` to the B2 endpoint.

## Project-specific conventions & patterns
- App layout is consistent: each app tends to have `models.py`, `views.py`, `forms.py`, `services.py` and `tests.py`. Prefer creating `services.py` for API/business logic (see `newsletter/services.py` and `pets/services.py` as examples).
- Custom user model: `AUTH_USER_MODEL = 'users.UsersMod'` — use `get_user_model()` in new code when referring to the user model.
- Tests rely on fixtures in `conftest.py`: use the existing `image_file`, `user`, and `superuser` fixtures to create users and file uploads in tests.
- Static/templates: global layout files under `base_templates/global/` and `base_static/global/` — change these when altering overall layout or styles.

## Integration points to be careful with
- External HTTP: MailerLite calls (timeout configured with `MAILERLITE_TIMEOUT`). Prefer to mock HTTP clients in unit tests (the repo already uses `httpx` in requirements).
- Storage and dev/prod divergence: code that reads/writes media must work with both `FileSystemStorage` (dev/tests) and `MediaStorage` (production). Tests use filesystem storage via `project/settings_test.py`.
- Database differences: tests use SQLite (see `project/settings_test.py`), local dev uses MySQL in Docker, and production uses Postgres — be mindful of SQL differences when writing queries or migrations.

## Quick file references (examples)
- Application entry: `manage.py`
- Primary settings: `project/settings.py` and test settings `project/settings_test.py`
- Docker: `Dockerfile`, `docker-compose.yml`, `start.sh`, `wait-for-db.sh`
- Tests: `pytest.ini`, `conftest.py`, app `tests.py` files
- Storage: `project/storage_backends.py` and `pets/storage_backends.py` (if present)

## Small coding guidelines for the agent
- Follow existing app structure: implement business logic in `services.py` and keep `views.py` thin.
- When adding migrations, run `python manage.py makemigrations` and keep migration files under the app's `migrations/` directory.
- Use `get_user_model()` rather than directly importing `users.UsersMod` to stay compatible with Django patterns.
- For tests, reuse fixtures from `conftest.py` and ensure uploaded files use the `image_file` fixture for ImageField/FileField tests.

## When editing infra or CI
- If you change static-file handling or storage backends, update `start.sh` and `Dockerfile` if you add runtime deps.
- Keep `pytest.ini` pointing to `project.settings_test` so CI uses the SQLite-backed test DB.

If anything here looks incomplete or you want more examples (for instance, typical `services.py` patterns or a list of common migrations), tell me which area to expand and I'll iterate.
