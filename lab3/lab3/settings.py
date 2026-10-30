# Wspólne ustawienia bez powielania konfiguracji Django.
from hub.settings import *

LAB_LEVEL = 3
INSTALLED_APPS = DJANGO_APPS + ['lab1.apps.Lab1Config', 'lab2.apps.Lab2Config', 'lab3.apps.Lab3Config']
ROOT_URLCONF = 'lab3.project_urls'
WSGI_APPLICATION = 'lab3.wsgi.application'
CSRF_FAILURE_VIEW = 'lab3.views.csrf_failure'
