from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Book


def index(request):
    return render(request, 'Lab_4/index.html')


@require_GET
def books_api(request):
    # QuerySet odczytuje dane z SQLite, a filtr wykonuje się w bazie.
    books = Book.objects.all()
    available = request.GET.get('available', '')
    if available == 'true':
        books = books.filter(available=True)
    elif available == 'false':
        books = books.filter(available=False)
    elif available != '':
        return JsonResponse({'error': 'Parametr available musi mieć wartość true lub false.'}, status=400)

    items = list(books.values('id', 'title', 'author', 'description', 'year', 'genre', 'available'))
    return JsonResponse({'items': items}, json_dumps_params={'ensure_ascii': False, 'indent': 2})
