from django.apps import AppConfig


class Lab1Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lab1'
    # Stara etykieta zachowuje tabele, uprawnienia i historię migracji.
    label = 'Lab_1'
