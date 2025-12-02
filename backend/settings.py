"""
Django settings for backend project (FranchiseHub).
Configured for Render + Supabase deployment.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
from django.contrib.messages import constants as messages
import cloudinary
import cloudinary.uploader
import cloudinary.api

# --------------------------------------------------------------------
# MANUALLY SET PATHS
# --------------------------------------------------------------------
# Project root (where manage.py is)
PROJECT_ROOT = Path.cwd()  # Current directory
# Django project folder
BASE_DIR = PROJECT_ROOT / "backend"

print(f"PROJECT_ROOT: {PROJECT_ROOT}")
print(f"BASE_DIR: {BASE_DIR}")

# --------------------------------------------------------------------
# LOAD ENVIRONMENT
# --------------------------------------------------------------------
# Check for .env in project root
env_path = PROJECT_ROOT / ".env"
if env_path.exists():
    
    load_dotenv(dotenv_path=env_path)
    print(f"✅ Loaded .env from: {env_path}")
else:
    print(f"❌ .env not found at: {env_path}")

# Debug what was loaded
print(f"DJANGO_DEBUG: {os.getenv('DJANGO_DEBUG')}")
print(f"RENDER: {os.getenv('RENDER')}")
print(f"DATABASE_URL exists: {'DATABASE_URL' in os.environ}")

# --- Debug/host config ---
DEBUG = os.getenv("DJANGO_DEBUG", "False").lower() == "true"
IS_RENDER = os.getenv('RENDER', '').lower() == 'true'
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME', '').strip() 

print(f"⚙️ IS_RENDER = {IS_RENDER}")
print(f"⚙️ DEBUG = {DEBUG}") 

# --------------------------------------------------------------------
# BASE CONFIGURATION
# --------------------------------------------------------------------
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

# CSRF trusted origins
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
    'cloudinary_storage',   
    'cloudinary',           
    "django.contrib.staticfiles",  
    "django_extensions",
    "accounts",
    
]
# Prevent caching
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middleware.NoCacheMiddleware',
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_ROOT / "templates"],  # Fixed: templates are in project root, not backend/
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.template.context_processors.static",
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
# --------------------------------------------------------------------
# DATABASE (Supabase for production, SQLite for local)
# --------------------------------------------------------------------
raw_db_url = os.environ.get("DATABASE_URL")

if raw_db_url:
    # Production: Supabase
    safe_db_url = raw_db_url.replace(":5432/", ":6543/")
    DATABASES = {
        "default": dj_database_url.config(
            default=safe_db_url,
            conn_max_age=0,
            ssl_require=True,
        )
    }
else:
    # Development: SQLite (local)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR.parent / 'db.sqlite3',
        }
    }

# --------------------------------------------------------------------
# VALIDATORS
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
STATIC_ROOT = BASE_DIR.parent / "staticfiles"
STATICFILES_DIRS = [BASE_DIR.parent / "static"]

if DEBUG:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
else:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# --------------------------------------------------------------------
# AUTH
# --------------------------------------------------------------------
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/accounts/browse/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# --------------------------------------------------------------------
# SESSION SECURITY
# --------------------------------------------------------------------
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 1209600

# --------------------------------------------------------------------
# CLOUDINARY CONFIG
# --------------------------------------------------------------------
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

# Validate Cloudinary credentials on Render
if IS_RENDER:
    if not all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
        raise ValueError(
            "Missing Cloudinary credentials! Please set CLOUDINARY_CLOUD_NAME, "
            "CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET in Render environment variables."
        )

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
    'API_KEY': CLOUDINARY_API_KEY,
    'API_SECRET': CLOUDINARY_API_SECRET,
    'SECURE': True,
}

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET,
    secure=True
)

# -----------------------------
# MEDIA FILES (Cloudinary for production, local for development)
# -----------------------------

if IS_RENDER:
    # Production: Cloudinary
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    # Cloudinary will handle MEDIA_URL automatically, don't override it
else:
    # Development: Local filesystem
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = PROJECT_ROOT / 'media'

print(f"DEBUG: DEFAULT_FILE_STORAGE = {DEFAULT_FILE_STORAGE}")
if not IS_RENDER:
    print(f"DEBUG: MEDIA_ROOT = {MEDIA_ROOT}")
    print(f"DEBUG: MEDIA_ROOT exists = {MEDIA_ROOT.exists()}")

# --------------------------------------------------------------------
# LOGGING - Capture all errors in production
# --------------------------------------------------------------------
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
