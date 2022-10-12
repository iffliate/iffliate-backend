from pathlib import Path
from telnetlib import AUTHENTICATION
from decouple import config
from datetime import timedelta 
import dj_database_url,os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = ["*",'https://0729-102-89-43-39.eu.ngrok.io']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'authentication',
    'djoser',
    'phonenumber_field',
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'django_filters',
    'product',
    'payment'
   
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    
]

ROOT_URLCONF = 'iffilate.urls'

AUTH_USER_MODEL = 'authentication.User'

REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY':'errors',
    'DEFAULT_AUTHENTICATION_CLASSES':[
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter', 
        'rest_framework.filters.OrderingFilter'
    ),
    'EXCEPTION_HANDLER': 'utils.custom_exception_response.custom_exception_handler',
}

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

WSGI_APPLICATION = 'iffilate.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {}
use_postgre = config('use_postgre',cast=bool)
if use_postgre:
    DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)  
    DATABASES['default'] = dj_database_url.config(default=config('DATABASE_URL'))
else:
     DATABASES['default']={
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / 'static'
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_FILE_STORAGE= 'cloudinary_storage.storage.MediaCloudinaryStorage'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CLOUDINARY_STORAGE={
    'CLOUD_NAME':config('CLOUD_NAME'),
    'API_KEY':config('API_KEY'),
    'API_SECRET':config('API_SECRET')    
}
white_list = ['http://localhost:8000/api/v1/auth/users/me','https://bucolic-travesseiro-b4154b.netlify.app/']
DJOSER = {
    'SEND_ACTIVATION_EMAIL': False,
    'ACTIVATION_URL':'/activate/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_URL':'/password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL':'/username/reset/confirm/{uid}/{token}',
    'PASSWORD_RESET_CONFIRM_RETYPE':True,
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND':True,
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': white_list
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME':timedelta(hours=24),
    'REFRESH_TOKEN_LIFETIME':timedelta(hours=24),
    'ROTATE_REFRESH_TOKENS':False,
    'BLACKLIST_AFTER_ROTATION':False,
    'ALGORITH':'HS256',
    'SIGNING_KEY':SECRET_KEY,
    'VERIFYING_KEY':None,
    'AUDIENCE':None,
    'ISSUER':None,
    'JWT_URL':None,
    'LEEWAY':0,
    
    'AUTH_HEADER_TYPES':('Bearer',),
    'AUTH_HEADER_NAME':'HTTP_AUTHORIZATION',
    'USER_ID_FIELD':'id',
    'USER_ID_CLAIM':'user_id',
    'USER_AUTHENTICATION_RULE':'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    
    # 'AUTH_TOKEN_CLASS':('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM':'token_type',
    'TOKEN_USER_CLASS':'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM':'jti',
    
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM':'refresh_ep',
    'SLIDING_TOKEN_REFRESH_LIFETIME':timedelta(hours=2),
    'SLIDING_TOKEN_LIFETIME':timedelta(hours=2)
}
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_CLIENTID')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_SECRET')


# corsheader related info

CORS_ALLOWED_ORIGINS = [
# frontend
"http://localhost:3000",# for nextjs localhost
'https://bucolic-travesseiro-b4154b.netlify.app',
'http://bucolic-travesseiro-b4154b.netlify.app',
# backend
"http://localhost:8000",
'https://bucolic-travesseiro-b4154b.netlify.app'
]

CORS_ALLOW_METHODS = [
'DELETE',
'GET',
'OPTIONS',
'PATCH',
'POST',
'PUT',
]

CORS_ALLOW_HEADERS = [
'accept',
'accept-encoding',
'authorization',
'content-type',
'dnt',
'origin',
'user-agent',
'x-csrftoken',
'x-requested-with',
]

CSRF_TRUSTED_ORIGINS =CORS_ALLOWED_ORIGINS



PAYSTACK_SECRET=os.environ['PAYSTACK_SECRET']
PAYSTACK_PUBLICKEY=os.environ['PAYSTACK_PUBLICKEY']