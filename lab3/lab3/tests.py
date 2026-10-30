import json

from django.test import Client, TestCase
from django.urls import reverse
from .models import Task


class TaskApiTests(TestCase):
    def setUp(self):
        self.index_url = reverse('Lab_3:index')
        self.list_url = reverse('Lab_3:task-list')
        self.client = Client(enforce_csrf_checks=True)
        self.client.get(self.index_url)
        self.token = self.client.cookies['csrftoken'].value

    def write(self, method, url=None, data=None, **headers):
        url = url or self.list_url
        return getattr(self.client, method)(
            url, data=json.dumps(data),
            content_type='application/json', HTTP_X_CSRFTOKEN=self.token, **headers,
        )

    def test_index_and_empty_list(self):
        response = self.client.get(self.index_url)
        self.assertContains(response, 'TaskBoard')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertEqual(self.client.get(self.list_url).json(), [])

    def test_create_and_persist(self):
        response = self.write('post', data={'title': '  Napisać raport  '})
        self.assertEqual(response.status_code, 201)
        task = Task.objects.get()
        self.assertEqual(task.title, 'Napisać raport')
        self.assertFalse(task.completed)
        self.assertIsNotNone(task.created_at)
        self.assertEqual(response.json()['id'], task.id)
        self.assertEqual(Client().get(self.list_url).json(), [response.json()])

    def test_invalid_titles_and_json_shapes(self):
        for data in [{}, {'title': ''}, {'title': ' \t\n'}, {'title': None},
                     {'title': 123}, {'title': True}, {'title': []},
                     {'title': 'a' * 201}, [], None, 'text',
                     {'title': 'Test', 'completed': True}]:
            with self.subTest(data=data):
                response = self.write('post', data=data)
                self.assertEqual(response.status_code, 400)
                self.assertIn('error', response.json())
        self.assertFalse(Task.objects.exists())

    def test_maximum_title_and_literal_markup(self):
        self.assertEqual(self.write('post', data={'title': 'a' * 200}).status_code, 201)
        text = '<img src=x onerror=alert(1)> Żółć'
        self.assertEqual(self.write('post', data={'title': text}).json()['title'], text)

    def test_malformed_json(self):
        for body in ['{', b'\xff']:
            response = self.client.post(self.list_url, data=body,
                                        content_type='application/json', HTTP_X_CSRFTOKEN=self.token)
            self.assertEqual(response.status_code, 400)

    def test_wrong_content_type(self):
        task = Task.objects.create(title='Test')
        for method, url in [('post', self.list_url), ('patch', f'{self.list_url}{task.id}/')]:
            response = getattr(self.client, method)(url, data='title=Test',
                content_type='text/plain', HTTP_X_CSRFTOKEN=self.token)
            self.assertEqual(response.status_code, 415)

    def test_toggle_both_directions(self):
        task = Task.objects.create(title='Test')
        for completed in [True, False]:
            response = self.write('patch', f'{self.list_url}{task.id}/', {'completed': completed})
            self.assertEqual(response.status_code, 200)
            task.refresh_from_db()
            self.assertEqual(task.completed, completed)
            self.assertEqual(response.json()['completed'], completed)

    def test_invalid_patch_does_not_modify_task(self):
        task = Task.objects.create(title='Test')
        for data in [{}, {'completed': 'false'}, {'completed': 0}, {'completed': None},
                     {'title': 'Nowy'}, {'completed': True, 'title': 'Nowy'}, []]:
            with self.subTest(data=data):
                response = self.write('patch', f'{self.list_url}{task.id}/', data)
                self.assertEqual(response.status_code, 400)
        task.refresh_from_db()
        self.assertEqual(task.title, 'Test')
        self.assertFalse(task.completed)

    def test_delete(self):
        task = Task.objects.create(title='Test')
        response = self.write('delete', f'{self.list_url}{task.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())
        self.assertFalse(Task.objects.exists())

    def test_missing_ids(self):
        for method in ['patch', 'delete']:
            for task_id in [0, 999999, 10 ** 30]:
                response = self.write(method, f'{self.list_url}{task_id}/', {'completed': True})
                self.assertEqual(response.status_code, 404)
                self.assertIn('error', response.json())

    def test_unsupported_methods(self):
        response = self.write('put', data={})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'GET, POST')
        response = self.client.get(self.list_url + '1/')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'PATCH, DELETE')

    def test_csrf_rejects_all_writes_without_token(self):
        task = Task.objects.create(title='Test')
        for method, url, data in [
            ('post', self.list_url, {'title': 'New'}),
            ('patch', f'{self.list_url}{task.id}/', {'completed': True}),
            ('delete', f'{self.list_url}{task.id}/', {}),
        ]:
            with self.subTest(method=method):
                response = getattr(self.client, method)(url, data=json.dumps(data), content_type='application/json')
                self.assertEqual(response.status_code, 403)
                self.assertIn('CSRF', response.json()['error'])
        task.refresh_from_db()
        self.assertFalse(task.completed)
        self.assertEqual(Task.objects.count(), 1)

    def test_csrf_rejects_wrong_token_and_foreign_origin(self):
        response = self.client.post(self.list_url, data='{}', content_type='application/json',
                                    HTTP_X_CSRFTOKEN='x' * 32)
        self.assertEqual(response.status_code, 403)
        response = self.write('post', data={'title': 'Test'}, HTTP_ORIGIN='https://example.net')
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Task.objects.exists())
