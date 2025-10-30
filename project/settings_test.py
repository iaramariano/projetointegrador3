from .settings import *  # noqa

# Banco de dados: SQLite para testes
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test_db.sqlite3",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
MEDIA_ROOT = BASE_DIR / "test_media"

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

DEBUG = False
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]
