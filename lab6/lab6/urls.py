from django.urls import path
from . import views

app_name = 'Lab_6'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/ksiazki/', views.books_api, name='books_api'),
    path('api/ksiazki/dodaj/', views.add_book, name='add_book'),
]
