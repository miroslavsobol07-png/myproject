from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import F
from lab4.models import Book


def index(request):
    genres = Book.objects.order_by('genre').values_list('genre', flat=True).distinct()
    return render(request, 'Lab_5/index.html', {'genres': genres})


@require_GET
def books_api(request):
    # pobieramy książki z bazy
    books = Book.objects.all()
    available = request.GET.get('available', '')
    if available == 'true':
        books = books.filter(available=True)
    elif available == 'false':
        books = books.filter(available=False)
    elif available != '':
        return JsonResponse({'error': 'Parametr available musi mieć wartość true lub false.'}, status=400)

    genre = request.GET.get('genre', '')
    if genre:
        books = books.filter(genre=genre)

    min_rating = request.GET.get('min_rating', '')
    if min_rating:
        if min_rating not in ['1', '2', '3', '4', '5']:
            return JsonResponse({'error': 'Minimalna ocena musi wynosić od 1 do 5.'}, status=400)
        books = books.filter(rating__gte=int(min_rating))

    # dozwolone pola sortowania
    sort = request.GET.get('sort', 'title')
    sorting = {
        'title': 'title',
        '-title': '-title',
        '-year': '-year',
        '-rating': F('rating').desc(nulls_last=True),
        '-added_on': F('added_on').desc(nulls_last=True),
    }
    if sort not in sorting:
        return JsonResponse({'error': 'Nieprawidłowy sposób sortowania.'}, status=400)
    books = books.order_by(sorting[sort], 'id')

    # ograniczamy liczbę wyników
    limit = request.GET.get('limit', '')
    if limit:
        try:
            limit = int(limit)
        except ValueError:
            return JsonResponse({'error': 'Limit musi być liczbą od 1 do 100.'}, status=400)
        if not 1 <= limit <= 100:
            return JsonResponse({'error': 'Limit musi być liczbą od 1 do 100.'}, status=400)
        books = books[:limit]

    items = list(books.values(
        'id', 'title', 'author', 'description', 'year', 'genre', 'available',
        'rating', 'added_on',
    ))
    return JsonResponse({'items': items}, json_dumps_params={'ensure_ascii': False, 'indent': 2})
