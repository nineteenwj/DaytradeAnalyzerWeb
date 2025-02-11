"""
Django settings for daytradeanalyzerweb project.

This file contains the settings and configuration for the project.
"""
import os
import yaml
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load configuration from config.yaml
CONFIG_FILE = os.path.join(BASE_DIR, 'config.yaml')
with open(CONFIG_FILE, 'r') as f:
    CONFIG = yaml.safe_load(f)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-qa4e0@s!stho-n!u3ot=xh=)m^%i+nl$khj!dc2=ma$hec8_-&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core', # my own app
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'core.middleware.AuthenticationMiddleware',  # 添加这行
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'daytradeanalyzerweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core', 'templates')],
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

WSGI_APPLICATION = 'daytradeanalyzerweb.wsgi.application'


# Database configuration: if storage_method is postgres, use it; otherwise, use SQLite.
if CONFIG.get('storage_method') == 'postgres':
    DATABASES = {
        'default': {
            'ENGINE': CONFIG.get('database').get('ENGINE'),
            'NAME': CONFIG.get('database').get('NAME'),
            'USER': CONFIG.get('database').get('USER'),
            'PASSWORD': CONFIG.get('database').get('PASSWORD'),
            'HOST': CONFIG.get('database').get('HOST'),
            'PORT': CONFIG.get('database').get('PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

AUTH_USER_MODEL = 'core.CustomUser'  # 使用自定义用户模型

LOGIN_URL = '/login/'  # 设置登录页面的URL
LOGIN_REDIRECT_URL = '/'  # 登录成功后的重定向URL

# 邮件设置（用于密码重置）
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'rss4kindle@qq.com'
EMAIL_HOST_PASSWORD = 'pdvemudtrazvdcef'

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
