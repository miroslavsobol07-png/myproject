from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Book


class CatalogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Testy używają oddzielnej bazy, więc nie zmieniają kolekcji użytkownika.
        for number in range(6):
            Book.objects.create(title=f'Książka {number}', author='Autor',
                                description='Opis', year=2020, genre='Powieść',
                                available=number < 4)
        cls.admin = User.objects.create_superuser('tester', '', 'TestoweHaslo2026!')

    def test_home(self):
        response = self.client.get(reverse('Lab_4:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Lab_4/index.html')
        self.assertContains(response, 'Wczytaj dane')

    def test_model(self):
        self.assertEqual(str(Book.objects.first()), 'Książka 0 – Autor')

    def test_api_json_and_types(self):
        response = self.client.get(reverse('Lab_4:books_api'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        items = response.json()['items']
        self.assertEqual(len(items), 6)
        self.assertEqual(set(items[0]), {'id', 'title', 'author', 'description', 'year', 'genre', 'available'})
        self.assertIs(type(items[0]['available']), bool)
        self.assertIs(type(items[0]['year']), int)
        self.assertIs(type(items[0]['title']), str)

    def test_available_filter(self):
        items = self.client.get(reverse('Lab_4:books_api'), {'available': 'true'}).json()['items']
        self.assertEqual(len(items), 4)
        self.assertTrue(all(book['available'] for book in items))

    def test_unavailable_filter(self):
        items = self.client.get(reverse('Lab_4:books_api'), {'available': 'false'}).json()['items']
        self.assertEqual(len(items), 2)
        self.assertTrue(all(not book['available'] for book in items))

    def test_invalid_filter(self):
        self.assertEqual(self.client.get(reverse('Lab_4:books_api'), {'available': 'xyz'}).status_code, 400)

    def test_empty_database(self):
        Book.objects.all().delete()
        self.assertEqual(self.client.get(reverse('Lab_4:books_api')).json(), {'items': []})

    def test_api_reads_database_changes(self):
        book = Book.objects.first()
        book.title = 'Nowy tytuł'
        book.available = False
        book.save()
        items = self.client.get(reverse('Lab_4:books_api')).json()['items']
        self.assertEqual(next(item for item in items if item['id'] == book.id)['title'], 'Nowy tytuł')
        self.assertEqual(len(self.client.get(reverse('Lab_4:books_api'), {'available': 'true'}).json()['items']), 3)

    def test_admin_requires_login(self):
        self.assertEqual(self.client.get('/admin/Lab_4/book/').status_code, 302)

    def test_admin_can_add_book(self):
        self.client.force_login(self.admin)
        response = self.client.post('/admin/Lab_4/book/add/', {
            'title': 'Dodana przez admina', 'author': 'Autor', 'description': 'Opis',
            'year': 2025, 'genre': 'Powieść', 'available': 'on', '_save': 'Zapisz',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(title='Dodana przez admina').exists())

    def test_api_rejects_post(self):
        self.assertEqual(self.client.post(reverse('Lab_4:books_api')).status_code, 405)
