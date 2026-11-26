import json
from django.test import Client, TestCase
from lab4.models import Book


class AddBookTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get('/lab6/')
        self.token = self.client.cookies['csrftoken'].value
        self.url = '/lab6/api/ksiazki/dodaj/'
        self.data = {
            'title': 'Nowa książka', 'author': 'Jan Kowalski',
            'description': 'Krótki opis', 'year': '2026', 'genre': 'Powieść',
            'available': True, 'rating': '4', 'added_on': '2026-11-27',
        }

    def post(self, data):
        return self.client.post(self.url, json.dumps(data),
                                content_type='application/json', HTTP_X_CSRFTOKEN=self.token)

    def test_valid_book_is_saved_and_returned_by_api(self):
        response = self.post(self.data)
        self.assertEqual(response.status_code, 201)
        book = Book.objects.get(pk=response.json()['id'])
        self.assertEqual(book.title, self.data['title'])
        self.assertEqual(book.rating, 4)
        items = self.client.get('/lab6/api/ksiazki/').json()['items']
        self.assertEqual(items[0]['id'], book.id)

    def test_missing_and_empty_fields(self):
        for field in ['title', 'author', 'description', 'year', 'genre']:
            for value in [None, '', '   ']:
                with self.subTest(field=field, value=value):
                    data = self.data.copy()
                    if value is None:
                        del data[field]
                    else:
                        data[field] = value
                    self.assertEqual(self.post(data).status_code, 400)
        self.assertEqual(Book.objects.count(), 0)

    def test_invalid_format_length_and_types(self):
        for field, value in [('title', 'a' * 151), ('author', 'a' * 101),
                             ('genre', 'a' * 61), ('year', 'abc'), ('year', '2.5'),
                             ('year', 0), ('year', 10000), ('year', True),
                             ('rating', 6), ('added_on', '2026-02-30'),
                             ('available', 'false'), ('title', ['abc']),
                             ('title', 123), ('rating', {'value': 4})]:
            with self.subTest(field=field, value=value):
                data = dict(self.data, **{field: value})
                response = self.post(data)
                self.assertEqual(response.status_code, 400)
                self.assertFalse(response.json()['ok'])
        self.assertEqual(Book.objects.count(), 0)

    def test_invalid_json_and_non_object(self):
        for body in ['{', '[]', 'null', '42', '"text"', b'\xff']:
            response = self.client.post(self.url, body, content_type='application/json',
                                        HTTP_X_CSRFTOKEN=self.token)
            self.assertEqual(response.status_code, 400)
        self.assertEqual(Book.objects.count(), 0)

    def test_csrf_is_required(self):
        for token in ['', 'wrong']:
            response = self.client.post(self.url, json.dumps(self.data),
                                        content_type='application/json', HTTP_X_CSRFTOKEN=token)
            self.assertEqual(response.status_code, 403)
        self.assertEqual(Book.objects.count(), 0)

    def test_only_post_is_allowed(self):
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_optional_fields_and_database_id(self):
        data = dict(self.data, rating='', added_on='', available=False, id=999999)
        response = self.post(data)
        self.assertEqual(response.status_code, 201)
        book = Book.objects.get()
        self.assertNotEqual(book.id, 999999)
        self.assertIsNone(book.rating)
        self.assertIsNone(book.added_on)
        self.assertFalse(book.available)

    def test_form_has_csrf_labels_and_no_id_field(self):
        response = self.client.get('/lab6/')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'for="id_title"')
        self.assertNotContains(response, 'name="id"')
