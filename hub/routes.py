from django.contrib import admin
from django.urls import include, path


def laboratory_urls(level):
    # Włączamy tylko bieżącą pracę i wcześniejsze, bez kopiowania ich kodu.
    from lab1 import views as first
    routes = [
        path('admin/', admin.site.urls),
        path('', first.hello, name='lab1_home'),
        path('lab1/', first.hello),
        path('lab1/', include('lab1.urls')),
        path('Lab_1/', first.hello),
        path('', include('lab1.urls')),
    ]
    if level >= 2:
        from lab2 import views as second
        routes = [
            path('', second.index, name='lab2_home'),
            path('lab2/', include('lab2.urls')),
            path('Lab_2/', include('lab2.urls')),
        ] + routes
    if level >= 3:
        from lab3 import views as third
        routes = [
            path('', third.index, name='lab3_home'),
            path('lab3/', include('lab3.urls', namespace='lab3')),
            path('Lab_3/', include('lab3.urls')),
            path('api/tasks/', third.task_list),
            path('api/tasks/<int:task_id>/', third.task_detail),
        ] + routes
    if level >= 4:
        from lab4 import views as fourth
        routes = [
            path('', fourth.index, name='lab4_home'),
            path('lab4/', include('lab4.urls', namespace='lab4')),
            path('Lab_4/', include('lab4.urls')),
        ] + routes
    return routes
