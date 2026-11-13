# Wyniki lokalne — laboratorium 5

Data sprawdzenia: 13 listopada 2026. Python 3.13.14, Django 5.2.18, Windows, Edge.

- Migracja `Lab_4.0002_book_rating_added_on`: OK.
- Porównanie z kopią SQLite sprzed migracji: wszystkie stare pola 6 książek są identyczne.
- Nowe pola uzupełniono w 6 książkach; oceny i daty są demonstracyjne.
- `manage.py check`: brak problemów.
- `makemigrations --check --dry-run`: brak niezapisanych zmian modelu.
- `manage.py test lab1 lab2 lab3 lab4 hub.tests`: 37 testów, OK.
- `collectstatic --noinput`: OK.
- Test Edge po zmianie wyglądu: lista 6 książek, nowe pola, cztery pola wyboru,
  łączenie dostępności, gatunku i oceny, sortowanie, limit API, JSON, brak wyników,
  telefon 390 px, błąd sieci i ponowne pobranie: OK.
- Podczas filtrowania strona nie została przeładowana; brak błędów JavaScript.
- Panel admina: lista 6 książek, oceny i daty oraz formularz edycji: OK.
- `git diff --check`: brak błędów białych znaków.

Zrzuty 01–06 pochodzą z lokalnego serwera:

1. `zrzuty/01_katalog.png`: cała kolekcja i nowe pola.
2. `zrzuty/02_filtry.png`: cztery dostępne książki posortowane po ocenie.
3. `zrzuty/03_json.png`: rzeczywista odpowiedź endpointu dla tych samych filtrów.
4. `zrzuty/04_telefon.png`: widok mobilny.
5. `zrzuty/05_admin.png`: lista w panelu administratora.
6. `zrzuty/06_admin_formularz.png`: nowe pola w formularzu istniejącej książki.

## Wdrożenie 13 listopada 2026

- Kod aplikacji: commit `98b80dd`, opublikowany na GitHub w gałęzi `main`.
- PythonAnywhere: pobrano kod przez `git pull --ff-only origin main`.
- Przed migracją wykonano serwerową kopię SQLite poza katalogiem projektu.
- Django 5.2.18: `check` bez błędów i 37 testów zakończonych powodzeniem.
- Migracja `Lab_4.0002_book_rating_added_on`: OK.
- Uzupełniono 6 książek; porównanie ze stanem sprzed migracji potwierdziło
  zachowanie wszystkich wcześniejszych pól tych 6 rekordów.
- `collectstatic`: 2 zaktualizowane pliki, 130 bez zmian; wykonano Web → Reload.
- Publiczna strona https://pi26msobol.pythonanywhere.com/lab4/ pokazuje 6 książek,
  cztery pola wyboru, Arial i szare karty.
- Po wybraniu dostępnych książek, gatunku Fantasy i oceny 5 wynik to Hobbit.
  Endpoint JSON zwraca ten sam rekord z oceną 5 i datą 2026-10-20.
- Potwierdzono strukturę `lab4/config/` (ustawienia), `lab4/lab4/` (kod)
  i `lab4/manage.py` na serwerze.
- `zrzuty/07_pythonanywhere.jpg`: strona po wdrożeniu.
- `zrzuty/08_pythonanywhere_filtry.jpg`: wynik połączenia filtrów na publicznym serwerze.

Finalne sprawozdanie PDF pozostaje do przygotowania według szablonu z danymi
studenta. Tabela punktacji pozostaje dla prowadzącej.
