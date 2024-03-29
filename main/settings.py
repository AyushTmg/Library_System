
from pathlib import Path
from datetime import timedelta
import os 



BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY =os.environ.get('SECRET_KEY')
DEBUG = True

ALLOWED_HOSTS = []

PROJECT_APP=[
    'authentication',
    'primary',
]

THIRD_PARTY_APP=[
    'rest_framework',
    'djoser',
    'django_filters',
    'django_celery_results',
    'django_celery_beat',
    "corsheaders",
    "debug_toolbar",
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]+PROJECT_APP+THIRD_PARTY_APP




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
     "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]


ROOT_URLCONF = 'main.urls'


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


WSGI_APPLICATION = 'main.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':os.environ.get('DB_NAME'),
        'USER': 'postgres', 
        'PASSWORD': os.environ.get('DB_PASS'), 
        'HOST': 'localhost', 

    }
}


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



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



# ! CONFIGURATIONS FOR STATIC FOLDER
STATIC_URL = 'static/'
STATICFILES_DIRS=[
    os.path.join(BASE_DIR,'static')
]

# ! CONFIGURATIONS FOR MEDIA FOLDER
MEDIA_URL='media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# !CONFIGURATIONS FOR DJANGO DEBUG TOOLBAR
INTERNAL_IPS = [
    "127.0.0.1",
]

# !CONFIGURATIONS FOR CUSTOME USER
AUTH_USER_MODEL='authentication.User'



# !CONFIGURATIONS FOR USING SIMPLE JWT
SIMPLE_JWT = {
   'AUTH_HEADER_TYPES': ('JWT',),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=10),
        "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}



# !CONFIGURATIONS FOR USING DJOSER
DJOSER={
    'SERIALIZERS':{
        'user':'authentication.serializers.UserSerializer',
        'current_user':'authentication.serializers.UserSerializer',
    },
    'LOGIN_FIELD':'email',
    'USER_CREATE_PASSWORD_RETYPE':True,
    'ACTIVATION_URL':'/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL':True,
    'SEND_CONFIRMATION_EMAIL':True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION':True,
    "PASSWORD_RESET_CONFIRM_URL": "email/reset/confirm/{uid}/{token}",
    'SET_PASSWORD_RETYPE':True,
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND':True,
    'TOKEN_MODEL':None,
    'USERNAME_RESET_CONFIRM_URL': '#/username/reset/confirm/{uid}/{token}',

}



# !For CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

# !Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' 
EMAIL_PORT = 587 
EMAIL_USE_TLS = True  
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD =os.environ.get('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL')


# !Celery Configurations 
CELERY_BROKER_URL='redis://localhost:6379/1'
CELERY_RESULT_BACKEND='django-db'
CELERY_RESULT_ENTENDED=True
CELERY_BEAT_SCHEDULER='django_celery_beat.schedulers.DatabaseScheduler'


