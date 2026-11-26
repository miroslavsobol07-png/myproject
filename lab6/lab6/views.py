import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from lab4.models import Book
from lab5.views import books_api
from .forms import BookForm


def index(request):
    genres = Book.objects.order_by('genre').values_list('genre', flat=True).distinct()
    return render(request, 'Lab_6/index.html', {'genres': genres, 'form': BookForm()})


@require_POST
def add_book(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'ok': False, 'error': 'Niepoprawny JSON.'}, status=400)

    if not isinstance(data, dict):
        return JsonResponse({'ok': False, 'error': 'Prześlij obiekt JSON.'}, status=400)

    for field in ['title', 'author', 'description', 'genre', 'added_on']:
        if field in data and not isinstance(data[field], str):
            return JsonResponse({'ok': False, 'error': 'Niepoprawne pole: ' + field}, status=400)
    for field in ['year', 'rating']:
        if field in data and type(data[field]) not in (str, int):
            return JsonResponse({'ok': False, 'error': 'Niepoprawne pole: ' + field}, status=400)
    if 'available' in data and type(data['available']) is not bool:
        return JsonResponse({'ok': False, 'error': 'Dostępność musi być true lub false.'}, status=400)

    form = BookForm(data)
    if not form.is_valid():
        errors = form.errors.get_json_data()
        messages = []
        for field, items in errors.items():
            label = form.fields[field].label
            messages.append(str(label) + ': ' + items[0]['message'])
        return JsonResponse({'ok': False, 'error': ' '.join(messages)}, status=400)

    book = form.save()
    return JsonResponse({'ok': True, 'id': book.id, 'title': book.title}, status=201)
