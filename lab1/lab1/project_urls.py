from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hello, name='lab1_home'),
    path('lab1/', views.hello),
    path('lab1/', include('lab1.urls')),
    path('Lab_1/', views.hello),
    path('', include('lab1.urls')),
]
