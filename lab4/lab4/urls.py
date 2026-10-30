from django.contrib import admin
from django.urls import path, include
from Lab_4 import views

urlpatterns = [
    # Główna strona również otwiera laboratorium.
    path('', views.index, name='home'),
    path('admin/', admin.site.urls),
    path('Lab_4/', include('Lab_4.urls')),
]
