from datetime import date
from io import StringIO

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

from lab4.models import Book


class Lab5Tests(TestCase):
    def test_lab4_and_lab5_use_same_books_with_different_fields(self):
        basic = self.client.get('/lab4/api/ksiazki/').json()['items']
        extended = self.client.get('/lab5/api/ksiazki/').json()['items']
        self.assertEqual([b['id'] for b in basic], [b['id'] for b in extended])
        self.assertNotIn('rating', basic[0])
        self.assertIn('rating', extended[0])
        self.assertIn('added_on', extended[0])

    def test_pages_load_their_own_assets_and_api(self):
        for number in [4, 5]:
            response = self.client.get(f'/lab{number}/')
            self.assertTemplateUsed(response, f'Lab_{number}/index.html')
            self.assertContains(response, f'/static/Lab_{number}/app.js')
            self.assertContains(response, f'/lab{number}/api/ksiazki/')

    @classmethod
    def setUpTestData(cls):
        cls.a = Book.objects.create(title='Alfa', author='Autor A', description='Opis A',
                                   year=2000, genre='Fantasy', available=True,
                                   rating=3, added_on=date(2026, 10, 1))
        cls.b = Book.objects.create(title='Beta', author='Autor B', description='Opis B',
                                   year=2020, genre='Fantasy', available=False,
                                   rating=5, added_on=date(2026, 11, 1))
        cls.c = Book.objects.create(title='Gamma', author='Autor C', description='Opis C',
                                   year=2010, genre='Powieść', available=True,
                                   rating=4, added_on=date(2026, 10, 15))
        cls.d = Book.objects.create(title='Delta', author='Autor D', description='Opis D',
                                   year=1990, genre='Powieść', available=True)
        cls.admin = User.objects.create_superuser('lab5tester', '', 'Lab5-test-only-2026!')

    def items(self, **params):
        response = self.client.get(reverse('Lab_5:books_api'), params)
        self.assertEqual(response.status_code, 200)
        return response.json()['items']

    def test_sorting_and_nulls_last(self):
        expected = {
            'title': [self.a, self.b, self.d, self.c],
            '-title': [self.c, self.d, self.b, self.a],
            '-year': [self.b, self.c, self.a, self.d],
            '-rating': [self.b, self.c, self.a, self.d],
            '-added_on': [self.b, self.c, self.a, self.d],
        }
        for sort, books in expected.items():
            with self.subTest(sort=sort):
                self.assertEqual([item['id'] for item in self.items(sort=sort)], [b.id for b in books])

    def test_combined_filters(self):
        items = self.items(genre='Fantasy', min_rating='4', available='false')
        self.assertEqual([item['id'] for item in items], [self.b.id])
        self.assertEqual(items[0]['rating'], 5)
        self.assertEqual(items[0]['added_on'], '2026-11-01')
        self.assertEqual(self.items(genre='Nieistniejący'), [])

    def test_filter_sort_and_limit_are_executed_by_database(self):
        with CaptureQueriesContext(connection) as queries:
            items = self.items(min_rating='3', sort='-rating', limit='2')
        self.assertEqual([item['id'] for item in items], [self.b.id, self.c.id])
        self.assertEqual(len(queries), 1)
        sql = queries[0]['sql'].upper()
        for clause in ['WHERE', 'ORDER BY', 'LIMIT 2']:
            self.assertIn(clause, sql)

    def test_invalid_parameters(self):
        for params in [{'available': 'yes'}, {'min_rating': '0'}, {'min_rating': '6'},
                       {'min_rating': 'abc'}, {'sort': 'password'}, {'limit': '0'},
                       {'limit': '-2'}, {'limit': '101'}, {'limit': '2.5'}, {'limit': 'abc'}]:
            with self.subTest(params=params):
                response = self.client.get(reverse('Lab_5:books_api'), params)
                self.assertEqual(response.status_code, 400)
                self.assertIn('error', response.json())

    def test_optional_fields_and_validation(self):
        item = next(item for item in self.items() if item['id'] == self.d.id)
        self.assertIsNone(item['rating'])
        self.assertIsNone(item['added_on'])
        self.d.full_clean()
        for rating in [0, 6]:
            self.d.rating = rating
            with self.assertRaises(ValidationError):
                self.d.full_clean()

    def test_admin_add_edit_and_invalid_rating(self):
        self.client.force_login(self.admin)
        data = {'title': 'Nowa książka', 'author': 'Autor', 'description': 'Opis',
                'year': 2026, 'genre': 'Fantasy', 'available': 'on',
                'rating': 4, 'added_on': '2026-11-04', '_save': 'Zapisz'}
        self.assertEqual(self.client.post('/admin/Lab_4/book/add/', data).status_code, 302)
        book = Book.objects.get(title='Nowa książka')
        self.assertEqual(book.rating, 4)
        self.assertEqual(book.added_on, date(2026, 11, 4))
        data['rating'] = 5
        self.assertEqual(self.client.post(f'/admin/Lab_4/book/{book.pk}/change/', data).status_code, 302)
        book.refresh_from_db()
        self.assertEqual(book.rating, 5)
        data['rating'] = 6
        response = self.client.post(f'/admin/Lab_4/book/{book.pk}/change/', data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('rating', response.context['adminform'].form.errors)
        book.refresh_from_db()
        self.assertEqual(book.rating, 5)

    def test_seed_preserves_existing_data_and_can_be_repeated(self):
        book = Book.objects.create(title='Hobbit', author='J.R.R. Tolkien',
                                   description='Mój opis', year=2001, genre='Fantasy',
                                   available=False, rating=2)
        for _ in range(2):
            call_command('uzupelnij_lab5', create_if_empty=True, stdout=StringIO())
        book.refresh_from_db()
        self.assertEqual(Book.objects.count(), 5)
        self.assertEqual(book.rating, 2)
        self.assertEqual(book.description, 'Mój opis')
        self.assertEqual(book.year, 2001)
        self.assertFalse(book.available)
        self.assertEqual(book.added_on, date(2026, 10, 20))

    def test_empty_database_setup(self):
        Book.objects.all().delete()
        call_command('uzupelnij_lab5', create_if_empty=True, stdout=StringIO())
        self.assertEqual(Book.objects.count(), 6)
        self.assertEqual(Book.objects.filter(rating__isnull=False, added_on__isnull=False).count(), 6)
