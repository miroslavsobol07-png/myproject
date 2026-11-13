# Laboratorium 5 — rozwinięcie katalogu z laboratorium 4

To dalszy ciąg aplikacji „Między stronami” z poprzedniego laboratorium.
Model `Book`, tabela `Lab_4_book`, wszystkie poprzednie pola i rekordy zostały zachowane.
Kod nadal znajduje się w `lab4/lab4`, a ustawienia w `lab4/config`.
Nie utworzono drugiej kolekcji ani kopii modelu. Adresy `/lab4/` i `/Lab_4/` działają nadal.

## Uruchomienie lokalne

Na tym komputerze, w PowerShell:

```powershell
cd C:\Users\miros\mojeZadania
& 'C:\Users\miros\Desktop\programowanie internetowe\.venv\Scripts\python.exe' manage.py runserver 8005
```

Strona: http://127.0.0.1:8005/lab4/
Panel: http://127.0.0.1:8005/admin/Lab_4/book/
API: http://127.0.0.1:8005/lab4/api/ksiazki/

Po pobraniu całego repozytorium na inny komputer:

```bash
python -m venv venv
# Aktywuj venv: Windows venv\Scripts\activate, Linux source venv/bin/activate
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py uzupelnij_lab5 --create-if-empty
python manage.py createsuperuser
python manage.py runserver 8005
```

Komenda `uzupelnij_lab5` uzupełnia tylko puste nowe pola sześciu znanych książek.
Rozpoznaje książki po tytule i autorze, a nie po numerze id. Nie nadpisuje własnych
ocen, dat ani wcześniejszych pól. Flaga `--create-if-empty` wczytuje książki z lab 4
wyłącznie wtedy, gdy kolekcja jest pusta. Oceny i daty są danymi demonstracyjnymi.
Własne książki można uzupełnić przez formularz administratora.

## Co zmieniłem

| Wymaganie | Realizacja |
|---|---|
| Dwa nowe pola | `rating`: opcjonalna liczba całkowita 1–5; `added_on`: opcjonalna data |
| Parametry pól | `null=True`, `blank=True`; ocena ma walidatory minimum i maksimum |
| Czytelne `__str__` | Zachowano tytuł i autora |
| Migracje | `lab4/lab4/migrations/0002_book_rating_added_on.py` dodaje dwie kolumny |
| Admin | Nowe kolumny i formularz, filtry, edycja oceny i dostępności na liście, nawigacja po dacie |
| Minimum 3 rekordy | Uzupełniono 6 istniejących książek |
| Sortowanie ORM | `Book.objects.all().order_by(...)` |
| Filtrowanie ORM | `filter(available=True)`, `filter(genre=...)`, `filter(rating__gte=...)` |
| Ograniczenie wyników | `books[:limit]` wykonuje SQL LIMIT |
| API GET | Zwraca 9 pól każdego rekordu w obiekcie `items` |
| Frontend | Cztery pola wyboru: dostępność, gatunek, ocena i sortowanie; fetch bez przeładowania strony |
| GitHub i PythonAnywhere | Aktualizacja tego samego repozytorium i istniejącej aplikacji; instrukcja poniżej |
| Sprawozdanie | Notatki i prawdziwe zrzuty lokalne w `materialy-lab5`; finalny PDF po wdrożeniu |

`blank=True` pozwala zostawić pole puste w formularzu. `null=True` pozwala
przechować brak wartości w bazie. Dzięki temu migracja nie wymaga wymyślania
ocen i dat dla starszych rekordów. Ocena jest sprawdzana przez formularze Django
i `full_clean()`; zwykłe `save()` nie wywołuje walidatorów automatycznie.

## Zapytania API do sprawdzenia

Podstawowy adres: `/lab4/api/ksiazki/`.

| Parametry | Wynik |
|---|---|
| `?sort=title` | Wszystkie książki według tytułu |
| `?available=true` | Dostępne książki |
| `?genre=Fantasy` | Książki wybranego gatunku |
| `?min_rating=4&sort=-rating` | Oceny od 4, najwyższe na początku |
| `?sort=-added_on&limit=3` | Trzy ostatnio dodane książki |
| `?available=true&min_rating=4&sort=-rating&limit=3` | Trzy najwyżej ocenione dostępne książki z oceną minimum 4 |

Na stronie są cztery pola wyboru: dostępność, gatunek, minimalna ocena i sortowanie,
oraz przycisk „Wczytaj dane”. Limit można sprawdzić przez adres API.
Dostępne sortowania API: `title`, `-title`, `-year`, `-rating`, `-added_on`.
Brak oceny lub daty jest na końcu odpowiedniego sortowania. Id rozstrzyga remisy.
Limit musi wynosić od 1 do 100, minimalna ocena od 1 do 5. Błędne parametry
zwracają JSON i HTTP 400; POST zwraca HTTP 405. Nieznany gatunek daje pustą listę.

## Testy

W korzeniu repozytorium, po aktywowaniu środowiska:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test lab1 lab2 lab3 lab4 hub.tests
python manage.py collectstatic --noinput
```

Wynik lokalny: **37 testów zakończonych powodzeniem**. Testy obejmują poprzednie
laboratoria, nowe pola, kombinacje filtrów, sortowanie, limit w zapytaniu SQL,
nieprawidłowe parametry, dodawanie i edycję w panelu oraz ponowne uruchamianie
komendy danych. Sprawdzono również zgodność wszystkich starych pól z kopią bazy
sprzed migracji: zachowano 6 z 6 książek.

Test przeglądarki: `node lab4/browser-test-lab5.cjs` przy serwerze na porcie 8005.
Wymaga Playwright i Edge; opcjonalna zmienna `PLAYWRIGHT_MODULE` wskazuje pakiet.
Oczekuje sześciu dostarczonych książek demonstracyjnych. Zapisuje prawdziwe zrzuty
do `lab4/materialy-lab5/zrzuty`. Sprawdza cztery pola wyboru, łączenie filtrów, limit API, JSON,
puste wyniki, szerokość mobilną, błąd sieci i ponowne pobranie.

## Publikacja

Repozytorium: https://github.com/miroslavsobol07-png/myproject, gałąź `main`.
Przed kolejną aktualizacją przejrzyj `git diff` i nowe pliki przez
`git status --short`, a następnie zapisz i wypchnij zatwierdzone zmiany.

Na PythonAnywhere źródła poprzedniej pracy są w:
`/home/PI26MSobol/pi26msobol.pythonanywhere.com`.
Najpierw wykonaj kopię serwerowej bazy, a następnie pobierz zatwierdzony kod.
Nie zastępuj serwerowej bazy lokalnym plikiem SQLite.

```bash
cd /home/PI26MSobol/pi26msobol.pythonanywhere.com
source /home/PI26MSobol/.virtualenvs/pi26msobol.pythonanywhere.com/bin/activate
# Po zatwierdzeniu i połączeniu zmian z main:
git pull --ff-only origin main
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py uzupelnij_lab5
python manage.py collectstatic --noinput
```

Uzupełnij minimum 3 książki własnymi wartościami w panelu, jeśli serwer nie ma
znanych książek demonstracyjnych. WSGI nadal korzysta z `hub.settings`, a static
z istniejącego `staticfiles`. Po Web → Reload sprawdź stronę, panel i powyższe
zapytania pod https://pi26msobol.pythonanywhere.com/lab4/.
Zapisz wyniki i zrzuty serwerowe, a następnie uzupełnij finalne sprawozdanie PDF
według szablonu. Tabela oceny pozostaje do uzupełnienia przez prowadzącą.

Dokumentacja: [migracje Django](https://docs.djangoproject.com/en/5.2/topics/migrations/)
i [wdrożenie na PythonAnywhere](https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/).
