import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Task


@ensure_csrf_cookie
def index(request):
    return render(request, 'Lab_3/index.html')


def task_data(task):
    return {
        'id': task.id,
        'title': task.title,
        'completed': task.completed,
        'created_at': task.created_at.isoformat(),
    }


def error(message, status=400):
    return JsonResponse({'error': message}, status=status)


def method_not_allowed(methods):
    response = error('Niedozwolona metoda HTTP.', 405)
    response['Allow'] = ', '.join(methods)
    return response


def read_json(request):
    if request.content_type != 'application/json':
        raise ValueError('Wyślij dane w formacie application/json.')
    try:
        data = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        raise ValueError('Nieprawidłowy JSON.')
    if not isinstance(data, dict):
        raise ValueError('Dane muszą być obiektem JSON.')
    return data


def task_list(request):
    if request.method == 'GET':
        return JsonResponse([task_data(task) for task in Task.objects.all()], safe=False)
    if request.method != 'POST':
        return method_not_allowed(['GET', 'POST'])
    if request.content_type != 'application/json':
        return error('Wyślij dane w formacie application/json.', 415)
    try:
        data = read_json(request)
        if set(data) != {'title'}:
            raise ValueError('Podaj wyłącznie pole title.')
        title = data['title']
        if not isinstance(title, str) or not title.strip():
            raise ValueError('Wpisz treść zadania.')
        title = title.strip()
        if len(title) > 200:
            raise ValueError('Zadanie może mieć najwyżej 200 znaków.')
    except ValueError as exc:
        return error(str(exc))
    task = Task.objects.create(title=title)
    return JsonResponse(task_data(task), status=201)


def task_detail(request, task_id):
    if request.method not in ['PATCH', 'DELETE']:
        return method_not_allowed(['PATCH', 'DELETE'])
    if task_id > 9223372036854775807:
        return error('Nie znaleziono zadania. Odśwież stronę.', 404)
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        return error('Nie znaleziono zadania. Odśwież stronę.', 404)
    if request.method == 'DELETE':
        task.delete()
        return JsonResponse({'message': 'Zadanie zostało usunięte.'})
    if request.content_type != 'application/json':
        return error('Wyślij dane w formacie application/json.', 415)
    try:
        data = read_json(request)
        if set(data) != {'completed'} or type(data['completed']) is not bool:
            raise ValueError('Pole completed musi mieć wartość true lub false.')
    except ValueError as exc:
        return error(str(exc))
    task.completed = data['completed']
    task.save(update_fields=['completed'])
    return JsonResponse(task_data(task))


def csrf_failure(request, reason=''):
    return error('Błąd CSRF. Odśwież stronę i spróbuj ponownie.', 403)
