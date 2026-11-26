from datetime import date

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from lab4.models import Book


class Command(BaseCommand):
    help = 'Uzupełnia puste nowe pola znanych książek przykładowymi danymi do lab 5.'

    def add_arguments(self, parser):
        parser.add_argument('--create-if-empty', action='store_true',
                            help='Wczytaj 6 książek z lab 4, tylko jeżeli kolekcja jest pusta.')

    @transaction.atomic
    def handle(self, *args, **options):
        if options['create_if_empty'] and not Book.objects.exists():
            call_command('loaddata', 'ksiazki', verbosity=0)

        # To dane demonstracyjne, a nie rzeczywiste oceny czy daty zakupu.
        samples = [
            ('Hobbit', 'J.R.R. Tolkien', 5, date(2026, 10, 20)),
            ('Mały Książę', 'Antoine de Saint-Exupéry', 4, date(2026, 10, 22)),
            ('Solaris', 'Stanisław Lem', 5, date(2026, 10, 25)),
            ('Duma i uprzedzenie', 'Jane Austen', 4, date(2026, 10, 27)),
            ('Tajemniczy ogród', 'Frances Hodgson Burnett', 3, date(2026, 10, 29)),
            ('W osiemdziesiąt dni dookoła świata', 'Jules Verne', 4, date(2026, 10, 30)),
        ]
        changed = 0
        for title, author, rating, added_on in samples:
            for book in Book.objects.filter(title=title, author=author):
                fields = []
                if book.rating is None:
                    book.rating = rating
                    fields.append('rating')
                if book.added_on is None:
                    book.added_on = added_on
                    fields.append('added_on')
                if fields:
                    book.save(update_fields=fields)
                    changed += 1
        self.stdout.write(self.style.SUCCESS(f'Uzupełniono książki: {changed}.'))
