# Laboratoria Django — lab1, lab2, lab3, lab4

Repozytorium zawiera własne, istniejące prace. Organizacja katalogów nawiązuje do
[przykładu hellodjango](https://github.com/SUBKREPER11/hellodjango); kod zadań nie został z niego skopiowany.

```text
myproject/
├── hub/                 # wspólne settings, urls, WSGI, ASGI i testy struktury
├── lab1/
│   ├── manage.py
│   └── lab1/            # widoki, urls, project_urls, settings, templates...
├── lab2/
│   ├── manage.py
│   └── lab2/            # własny kod, templates i static
├── lab3/
│   ├── manage.py
│   └── lab3/            # TaskBoard, API, migracje, templates i static
├── lab4/
│   ├── manage.py
│   └── lab4/            # książki, API, admin, migracje, templates i static
├── manage.py            # uruchamia cały hub
├── requirements.txt
└── db.sqlite3           # istniejąca baza; nie trafia do Git
```

## Co zawierają kolejne prace

| Uruchomiony katalog | Dostępna funkcjonalność |
|---|---|
| lab1 | powitanie, imię, szablon, aktualny czas |
| lab2 | lab1 + strona HTML/CSS |
| lab3 | lab1 + lab2 + TaskBoard: dodawanie, oznaczanie, usuwanie i API JSON |
| lab4 | lab1 + lab2 + lab3 + katalog książek, admin, fetch i filtrowanie |
| hub (korzeń) | wszystkie cztery prace |

Kod wcześniejszych prac jest współdzielony. Każde `settings.py` włącza tylko
potrzebne aplikacje, a `project_urls.py` dołącza trasy poprzedniej pracy.
`urls.py` zawiera własne adresy aplikacji. Pobierz całe repozytorium, nie sam
podkatalog — późniejsze prace celowo korzystają z wcześniejszych.

Nazwy pakietów to `lab1`–`lab4`, ale `AppConfig.label` pozostaje `Lab_1`–`Lab_4`.
Dzięki temu istniejące tabele, migracje, uprawnienia i adresy admina nie zmieniają
się. Wszystkie warianty korzystają ze wspólnej bazy w korzeniu repozytorium.

## Uruchomienie

W korzeniu repozytorium, po aktywowaniu środowiska z Pythonem 3.10 lub nowszym:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 8000
```

Jeżeli nie masz środowiska, utwórz je raz przez `python -m venv venv`.
Aktywacja Windows: `venv\Scripts\activate`; Linux: `source venv/bin/activate`.
Środowisko i baza są wykluczone przez `.gitignore`.

Każdą pracę można uruchomić osobno, również z jej katalogu:

```bash
python lab1/manage.py runserver 8001
python lab2/manage.py runserver 8002
python lab3/manage.py runserver 8003
python lab4/manage.py runserver 8004
```

Te cztery polecenia uruchamia się w osobnych terminalach. Strona główna danego
portu pokazuje bieżącą pracę; wcześniejsze są dostępne pod adresami poniżej.

| Praca | Adresy (np. http://127.0.0.1:8000) |
|---|---|
| lab1 | `/lab1/`, `/hello/`, `/hello/Anna/`, `/hello_template/Anna/`, `/time/` |
| lab2 | `/lab2/` |
| lab3 | `/lab3/`, `/api/tasks/` |
| lab4 | `/lab4/`, `/lab4/api/ksiazki/?available=true`, `/admin/` |

Dotychczasowe `/Lab_2/`, `/Lab_3/` i `/Lab_4/` też działają.
Templates i static są wewnątrz aplikacji, z zachowanymi nazwami `Lab_1` itd.
Django wyszukuje je przez `APP_DIRS` i `AppDirectoriesFinder`.

Przy **nowej, pustej bazie** można wykonać `python manage.py loaddata ksiazki`
oraz `python manage.py createsuperuser`. Nie ładuj fixture przy aktualizacji
istniejącej kolekcji, bo mogłaby nadpisać rekordy o tych samych id.

## Sprawdzenie

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test lab1 lab2 lab3 lab4 hub.tests
python lab1/manage.py test lab1 hub.tests
python lab2/manage.py test lab1 lab2 hub.tests
python lab3/manage.py test lab1 lab2 lab3 hub.tests
python lab4/manage.py test lab1 lab2 lab3 lab4 hub.tests
python manage.py collectstatic --noinput
```

Testy API zapisują dane tylko w osobnej bazie testowej, nie w bazie użytkownika.

## PythonAnywhere

Strona: https://pi26msobol.pythonanywhere.com/lab4/

Katalog źródeł: `/home/PI26MSobol/pi26msobol.pythonanywhere.com/Lab_4`.
Zewnętrzna nazwa katalogu pozostała, ale jego zawartość odpowiada korzeniowi
tego repozytorium: `hub`, `lab1`, `lab2`, `lab3`, `lab4`, `manage.py`.

Aktualizacja po wdrożeniu tej struktury:

```bash
cd /home/PI26MSobol/pi26msobol.pythonanywhere.com/Lab_4
source /home/PI26MSobol/.virtualenvs/pi26msobol.pythonanywhere.com/bin/activate
git pull --ff-only origin main
python -m pip install -r requirements.txt
python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
```

Następnie Web → Reload. WSGI używa `hub.settings`. Produkcyjny `DJANGO_SECRET_KEY`
jest zachowany poza Git, a `DJANGO_DEBUG=0`. `/static/` wskazuje na
`/home/PI26MSobol/pi26msobol.pythonanywhere.com/Lab_4/staticfiles`.
Nie kopiuj lokalnej bazy na serwer i nie usuwaj serwerowej bazy przy aktualizacji.

Jeśli na serwerze nie ma konta administratora, wykonaj w tym samym katalogu
`python manage.py createsuperuser` i ustaw własne dane logowania. Ta komenda
nie usuwa książek ani zadań. Lokalny administrator nie jest automatycznie
kopiowany na PythonAnywhere.
