"""
Django settings for backend project (FranchiseHub).
Configured for Render + Supabase deployment.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
from django.contrib.messages import constants as messages

# --------------------------------------------------------------------
# BASE CONFIGURATION
# --------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables (.env for local dev, Render vars for prod)
if os.environ.get("RENDER", "") != "true":
    load_dotenv(dotenv_path=BASE_DIR / ".env")

# --- Debug/host config ---
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"
IS_RENDER = os.getenv('RENDER', '').lower() == 'true'
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME', '').strip()

# When running on Render, set ALLOWED_HOSTS from RENDER_EXTERNAL_HOSTNAME automatically
if DEBUG:
    ALLOWED_HOSTS = []
else:
    env_hosts = [
        h.strip()
        for h in os.getenv('ALLOWED_HOSTS', '').split(',')
        if h.strip()
    ]

    ALLOWED_HOSTS = env_hosts or [
        "127.0.0.1",
        "localhost",
        RENDER_EXTERNAL_HOSTNAME,
    ]


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
    'cloudinary',
    'cloudinary_storage',
]

# ✅ ADD MIDDLEWARE TO PREVENT CACHING OF AUTHENTICATED PAGES
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middleware.NoCacheMiddleware',  # ✅ Add custom middleware
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
raw_db_url = os.environ.get("DATABASE_URL")

if raw_db_url is None:
    raise ValueError("❌ ERROR: DATABASE_URL environment variable is missing!")

# Force Django to use Transaction Pooler instead of Session Pooler
safe_db_url = raw_db_url.replace(":5432/", ":6543/")

DATABASES = {
    "default": dj_database_url.config(
        default=safe_db_url,
        conn_max_age=0,
        ssl_require=True,
    )
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

# Message framework tags mapped to Bootstrap 5 classes
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ SESSION SECURITY SETTINGS
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
SESSION_COOKIE_SECURE = not DEBUG  # Use HTTPS in production
SESSION_COOKIE_SAMESITE = 'Lax'  # CSRF protection
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Keep session after browser close
SESSION_COOKIE_AGE = 1209600  # 2 weeks

import os
import cloudinary
import cloudinary.uploader
import cloudinary.api

# ✅ FIXED: Cloudinary Configuration with HTTPS enforcement
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
    'SECURE': True,  # ✅ Force HTTPS URLs
}

# Configure cloudinary with HTTPS
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True  # ✅ This ensures all URLs use HTTPS
)

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
