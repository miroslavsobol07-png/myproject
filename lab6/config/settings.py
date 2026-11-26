from hub.settings import *

LAB_LEVEL = 6
INSTALLED_APPS = DJANGO_APPS + ['lab1.apps.Lab1Config', 'lab2.apps.Lab2Config', 'lab3.apps.Lab3Config', 'lab4.apps.Lab4Config', 'lab5.apps.Lab5Config', 'lab6.apps.Lab6Config']
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
CSRF_FAILURE_VIEW = 'lab3.views.csrf_failure'
