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

Zrzuty pochodzą z lokalnego serwera, a nie z PythonAnywhere:

1. `zrzuty/01_katalog.png`: cała kolekcja i nowe pola.
2. `zrzuty/02_filtry.png`: cztery dostępne książki posortowane po ocenie.
3. `zrzuty/03_json.png`: rzeczywista odpowiedź endpointu dla tych samych filtrów.
4. `zrzuty/04_telefon.png`: widok mobilny.
5. `zrzuty/05_admin.png`: lista w panelu administratora.
6. `zrzuty/06_admin_formularz.png`: nowe pola w formularzu istniejącej książki.

GitHub, migracja na PythonAnywhere i testy po wdrożeniu pozostają do wykonania
po akceptacji użytkownika. Finalne sprawozdanie PDF należy uzupełnić wynikami
wdrożenia i danymi studenta; tabela punktacji pozostaje dla prowadzącej.
