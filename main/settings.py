
import os 
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-=vr7kort91m#4-eivch*py$dh*342@--*x6qze+&@c_the2cdx'

DEBUG = True

ALLOWED_HOSTS = []


# !FOR SPECIFYING THIRD PROJECT APPS
PROJECT_APPS=[
    'authentication',
    'library'
]


# !FOR SPECIFYING THIRD PARTY APPS 
THIRD_PARTY_APPS=[
    "debug_toolbar",
    'rest_framework',
    'rest_framework_simplejwt',
]


# !INSTALLED APP'S
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

]

#! APPEND PROJECT APP AND THIRD PARTY APPS INTO INSTALLED APPS
INSTALLED_APPS+=PROJECT_APPS
INSTALLED_APPS+=THIRD_PARTY_APPS


# !DJANGO DEBUG TOOLBAR CONFIGURATION'S
INTERNAL_IPS = [
    "127.0.0.1",
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware", #DJANGO DEBUG TOOLBAR MIDDLEWARE
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



# !DEFAULT DATABASE CONFIGURATION'S 
"""
If You dont want to use postgres as your database 
You can use this instead just uncomment this one 
and comment or remove the one beneth it 
"""
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# !DATABASE CONFIGURATION'S FOR POSTGRE'S
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':os.environ.get("DB_NAME"),
        'USER': 'postgres', 
        'PASSWORD':os.environ.get("DB_PASS"), 
        'HOST': 'localhost', 

    }
}

# ! CONFIGURATION'S FOR CUSTOM USER MODEL
AUTH_USER_MODEL='authentication.User'


# ! SIMPLE JWT CONFIGURATION'S
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}



# ! SIMPLE JWT CONFIGURATION'S
SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT'),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=60),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
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


STATIC_URL = 'static/'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
