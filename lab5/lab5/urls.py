from django.urls import path
from . import views

app_name = 'Lab_5'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/ksiazki/', views.books_api, name='books_api'),
]
