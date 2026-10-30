# Wspólne ustawienia bez powielania konfiguracji Django.
from hub.settings import *

LAB_LEVEL = 2
INSTALLED_APPS = DJANGO_APPS + ['lab1.apps.Lab1Config', 'lab2.apps.Lab2Config']
ROOT_URLCONF = 'lab2.project_urls'
WSGI_APPLICATION = 'lab2.wsgi.application'
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'
