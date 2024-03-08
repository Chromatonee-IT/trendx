
from pathlib import Path
from django.contrib.messages import constants as messages
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MESSAGE_TAGS = {
    messages.SUCCESS: 'alert-success',
    messages.ERROR: 'alert-danger',
    messages.INFO: 'alert-info'
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '()6f$@712andea35dnw^kmaps8u%kc))p%%^%3i+3h6*hob)wq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# CSRF_TRUSTED_ORIGINS = ['https://*.cartnbuy.in','.cartnbuy.in']

# Application definition

INSTALLED_APPS = [
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'store.apps.StoreConfig',
    'vendor.apps.VendorConfig',
    'storages',
    'trendx',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',

]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "https://4883-45-120-18-138.ngrok-free.app",
  # Replace with your frontend's URL during development
    # Add more origins as needed
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'


ROOT_URLCONF = 'trendx.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'trendx.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'cartandbuy',
#         'USER': 'cartandbuy',
#         'PASSWORD': 'cartandbuy',
#         'HOST': 'database.cpk4o8s449a3.eu-north-1.rds.amazonaws.com',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT='staticfiles'

MEDIA_DIR =  BASE_DIR/ 'media'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
BASE_URL = 'https://cartnbuy.in'

# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.in'  # Your SMTP server
EMAIL_PORT = 587  # Your SMTP port (587 for TLS, 465 for SSL)
EMAIL_USE_TLS = True  # Use TLS (True/False)
EMAIL_HOST_USER = 'support@cartnbuy.in'  # Your email address
EMAIL_HOST_PASSWORD = 'Cartandbuy@123'  # Your email password



# AWS_ACCESS_KEY_ID = 'AKIAZQ3DSUSVKSU5RYK4'
# AWS_SECRET_ACCESS_KEY = 'YQcHAA2tmTvl6dKYJ+8o8krzENLWvBBjkJvNR3LT'
# AWS_STORAGE_BUCKET_NAME = 's3cartandbuy'
# AWS_S3_SIGNATURE_NAME = 's3v4'
# AWS_S3_REGION_NAME = 'us-east-2'
# AWS_S3_FILE_OVERRITE = False
# AWS_DEFAULT_ACL = None
# AWS_S3_VERITY = True
# DEFAULT_FILE_ST0RAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# STORAGES = {
# 	"default": {
# 		"BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
#     },
# 	"staticfiles": {
# 		"BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
#     },
# }

# MEDIA_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
# MEDIA_ROOT = ''
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'