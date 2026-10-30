from django.urls import include, path
from lab2.project_urls import urlpatterns as previous_urls
from . import views

urlpatterns = [
    path('', views.index, name='lab3_home'),
    path('lab3/', include('lab3.urls', namespace='lab3')),
    path('Lab_3/', include('lab3.urls')),
    path('api/tasks/', views.task_list),
    path('api/tasks/<int:task_id>/', views.task_detail),
] + previous_urls
