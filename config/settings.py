from pathlib import Path
from decouple import config
import os 

BASE_DIR = Path(__file__).resolve().parent.parent

deploy = True
if(deploy):
    # deploy
    SECRET_KEY = os.getenv('SECRET_KEY', 'LIARA_URL is not set.')
    shop_email = os.getenv('EMAIL_HOST', 'LIARA_URL is not set.')
    password_email = os.getenv('EMAIL_HOST_PASSWORD', 'LIARA_URL is not set.')
    merchant = os.getenv('MERCHANT', 'LIARA_URL is not set.')
    DEBUG = os.getenv('DEBUG', 'LIARA_URL is not set.')
    admin_url = os.getenv('ADMIN', 'LIARA_URL is not set.')
    ip_find = os.getenv('IPFIND', 'LIARA_URL is not set.')
    SMS_PASSWORD = os.getenv('SMS_PASSWORD', 'LIARA_URL is not set.')
    ADMIN_PHONE = os.getenv('ADMIN_PHONE', 'LIARA_URL is not set.')
else:
    # local
    SECRET_KEY = config('SECRET_KEY')
    shop_email = config('EMAIL_HOST')
    password_email = config('EMAIL_HOST_PASSWORD')
    merchant = config('MERCHANT')
    admin_url = config('ADMIN')
    ip_find = config('IPFIND')
    SMS_PASSWORD = config('SMS_PASSWORD')
    ADMIN_PHONE = config('ADMIN_PHONE')
    DEBUG = True

    connect_server = config('CONNECT')

    database_name = config('DB_Name')
    database_username = config('DB_USERNAME')
    password = config('DB_PASSWORD')
    database_hostname_or_ip = config('DB_HOST')
    database_port = config('DB_PORT')


ALLOWED_HOSTS = []




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


INSTALLED_APPS += [
    'facades',
    'stuff',
    'accounts',
    'cart',
    'orders',
    'blog',
    'django_cleanup.apps.CleanupConfig',
    'administratorship',
    'tracking',
    'ipware',
    'admin_honeypot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tracking.middleware.UserVisitMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


if(deploy):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('database_name', 'LIARA_URL is not set.'),
            'USER': os.getenv('database_username', 'LIARA_URL is not set.'),
            'PASSWORD': os.getenv('password', 'LIARA_URL is not set.'),
            'HOST': os.getenv('database_hostname_or_ip', 'LIARA_URL is not set.'),
            'PORT': os.getenv('database_port', 'LIARA_URL is not set.'),
        }
    }
else:
    if connect_server == '0':
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': database_name,
                'USER': database_username,
                'PASSWORD': password,
                'HOST': database_hostname_or_ip,
                'PORT': database_port
            }
        }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'
