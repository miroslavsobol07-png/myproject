from django.urls import include, path
from lab3.project_urls import urlpatterns as previous_urls
from . import views

urlpatterns = [
    path('', views.index, name='lab4_home'),
    path('lab4/', include('lab4.urls', namespace='lab4')),
    path('Lab_4/', include('lab4.urls')),
] + previous_urls
