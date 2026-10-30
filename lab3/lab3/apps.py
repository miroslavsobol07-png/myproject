from django.apps import AppConfig


class Lab3Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'lab3'
    # Stara etykieta zachowuje tabele, uprawnienia i historię migracji.
    label = 'Lab_3'
