from django.urls import include, path
from lab1.project_urls import urlpatterns as previous_urls
from . import views

# Najpierw strona aktualnej pracy, potem cała poprzednia praca.
urlpatterns = [
    path('', views.index, name='lab2_home'),
    path('lab2/', include('lab2.urls')),
    path('Lab_2/', include('lab2.urls')),
] + previous_urls
