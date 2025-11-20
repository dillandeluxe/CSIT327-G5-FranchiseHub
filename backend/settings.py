"""
Django settings for backend project (FranchiseHub).
Configured for Render + Supabase deployment.
"""

import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
from dotenv import load_dotenv
import dj_database_url

# --------------------------------------------------------------------
# BASE CONFIGURATION
# --------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables (.env for local dev, Render vars for prod)
if os.environ.get("RENDER", "") != "true":
    load_dotenv(dotenv_path=BASE_DIR / ".env")

# --- Debug/host config ---
DEBUG = os.getenv('DJANGO_DEBUG', 'True').lower() == 'true'
IS_RENDER = os.getenv('RENDER', '').lower() == 'true'
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME', '').strip()

# When running on Render, set ALLOWED_HOSTS from RENDER_EXTERNAL_HOSTNAME automatically
if DEBUG:
    ALLOWED_HOSTS = []
else:
    env_hosts = [h.strip() for h in os.getenv('ALLOWED_HOSTS', '').split(',') if h.strip()]
    ALLOWED_HOSTS = env_hosts or ([RENDER_EXTERNAL_HOSTNAME] if RENDER_EXTERNAL_HOSTNAME else [])

# CSRF trusted origins (include Render URL if available)
default_csrf = []
if RENDER_EXTERNAL_HOSTNAME:
    default_csrf.append(f"https://{RENDER_EXTERNAL_HOSTNAME}")
CSRF_TRUSTED_ORIGINS = default_csrf + [
    o.strip() for o in os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()
]

# --------------------------------------------------------------------
# SECURITY
# --------------------------------------------------------------------
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "unsafe-dev-key")

# --------------------------------------------------------------------
# APPLICATIONS
# --------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # keep directly after SecurityMiddleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "accounts.middleware.AdminAuthorizationMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.template.context_processors.static",  # NEW: ensures {% static %} has context
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

# --------------------------------------------------------------------
# DATABASE (Supabase)
# --------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --------------------------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --------------------------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Manila"
USE_I18N = True
USE_TZ = True

# --------------------------------------------------------------------
# STATIC FILES
# --------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"  # collectstatic output
STATICFILES_DIRS = [BASE_DIR / "static"]  # source assets for development

# Use simpler storage in dev; hashed, compressed files in production
if DEBUG:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
else:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Optional (recommended on Render behind proxy)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# --------------------------------------------------------------------
# AUTHENTICATION & LOGIN
# --------------------------------------------------------------------
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/accounts/browse/"

# --------------------------------------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# --------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
