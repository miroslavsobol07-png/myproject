from django.conf import settings
from django.contrib.staticfiles import finders
from django.test import TestCase
from django.urls import Resolver404, resolve


class LaboratoryStructureTests(TestCase):
    # Te same testy sprawdzają osobno lab1, lab2, lab3, lab4 i hub.
    def test_previous_pages_are_available(self):
        paths = ['/hello/', '/hello/Anna/', '/hello_template/Anna/', '/time/']
        paths += [f'/lab{i}/' for i in range(1, settings.LAB_LEVEL + 1)]
        for path in paths:
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_home_shows_current_laboratory(self):
        response = self.client.get('/')
        if settings.LAB_LEVEL == 1:
            self.assertContains(response, 'Witaj w Django!')
        else:
            self.assertTemplateUsed(response, f'Lab_{settings.LAB_LEVEL}/index.html')

    def test_future_laboratories_are_not_enabled(self):
        for number in range(settings.LAB_LEVEL + 1, 5):
            self.assertNotIn(f'lab{number}.apps.Lab{number}Config', settings.INSTALLED_APPS)
            with self.assertRaises(Resolver404):
                resolve(f'/lab{number}/')

    def test_static_files_and_admin(self):
        self.assertEqual(self.client.get('/admin/login/').status_code, 200)
        for number in range(2, settings.LAB_LEVEL + 1):
            self.assertIsNotNone(finders.find(f'Lab_{number}/style.css'))
        for number in range(3, settings.LAB_LEVEL + 1):
            self.assertIsNotNone(finders.find(f'Lab_{number}/app.js'))

    def test_existing_api_addresses(self):
        if settings.LAB_LEVEL >= 3:
            for path in ['/api/tasks/', '/Lab_3/api/tasks/', '/lab3/api/tasks/']:
                self.assertEqual(self.client.get(path).json(), [])
        if settings.LAB_LEVEL >= 4:
            for path in ['/Lab_4/api/ksiazki/', '/lab4/api/ksiazki/']:
                self.assertEqual(self.client.get(path).json(), {'items': []})
