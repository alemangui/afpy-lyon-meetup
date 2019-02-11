"""
Django settings for meetup project. Generated by 'django-admin startproject' 
using Django 2.1.5.
"""

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '***********************'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition
ROOT_URLCONF = 'meetup.urls'
WSGI_APPLICATION = 'meetup.wsgi.application'

# Celery
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672/'
CELERY_TASK_ALWAYS_EAGER = False
CELERY_CREATE_MISSING_QUEUES = True
CELERY_RESULT_BACKEND = 'rpc'