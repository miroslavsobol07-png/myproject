from django.apps import AppConfig


class Lab2Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lab2'
    # Stara etykieta zachowuje tabele, uprawnienia i historię migracji.
    label = 'Lab_2'
