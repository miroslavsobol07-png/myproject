# Wspólne ustawienia bez powielania konfiguracji Django.
from hub.settings import *

LAB_LEVEL = 1
INSTALLED_APPS = DJANGO_APPS + ['lab1.apps.Lab1Config']
ROOT_URLCONF = 'lab1.project_urls'
WSGI_APPLICATION = 'lab1.wsgi.application'
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'
