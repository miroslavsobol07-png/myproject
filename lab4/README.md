# Lab_4 — katalog książek

Istniejący projekt po uporządkowaniu katalogów. Nazwa aplikacji `Lab_4` została
zachowana, aby nie zmieniać tabeli `Lab_4_book`, migracji i adresów.

```text
lab4/
├── lab4/             # settings.py, urls.py, wsgi.py, asgi.py
├── Lab_4/            # models.py, views.py, admin.py, migrations, tests.py
├── templates/Lab_4/index.html
├── static/Lab_4/     # style.css i app.js
├── manage.py
├── requirements.txt
└── db.sqlite3        # istniejąca baza, tylko lokalnie; nie w Git
```

## Uruchomienie na tym komputerze

W terminalu VS Code otwartym w tym katalogu:

```powershell
..\.venv\Scripts\python.exe manage.py runserver 8006
```

Strona: http://127.0.0.1:8006/ lub http://127.0.0.1:8006/Lab_4/.
API: http://127.0.0.1:8006/Lab_4/api/ksiazki/.
Admin: http://127.0.0.1:8006/admin/. Istniejące konto i książki zostały zachowane.

## Uruchomienie po pobraniu z GitHub

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe manage.py migrate
.\venv\Scripts\python.exe manage.py loaddata ksiazki
.\venv\Scripts\python.exe manage.py createsuperuser
.\venv\Scripts\python.exe manage.py runserver
```

`loaddata` jest potrzebne tylko przy tworzeniu nowej bazy. Nie wykonuj go przy
aktualizacji istniejącej kolekcji — może nadpisać rekordy o tych samych id.

## Sprawdzenie

```powershell
..\.venv\Scripts\python.exe manage.py check
..\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
..\.venv\Scripts\python.exe manage.py test Lab_4
..\.venv\Scripts\python.exe manage.py collectstatic --noinput
```

`templates` jest wskazane w `TEMPLATES[0]['DIRS']`, a `static` w
`STATICFILES_DIRS`. `staticfiles` to katalog wynikowy collectstatic, nie źródła.
Środowiska, baza, logi, sekrety i staticfiles są wykluczone przez .gitignore.

## PythonAnywhere

Opublikowana strona: https://pi26msobol.pythonanywhere.com/Lab_4/.
Na istniejącym koncie Lab_4 działa w projekcie `mojProjekt` obok wcześniejszych
laboratoriów. HTML znajduje się w `templates/Lab_4/`, CSS i JS w `static/Lab_4/`,
w katalogu `/home/PI26MSobol/pi26msobol.pythonanywhere.com`.
Baza i WSGI tego wspólnego projektu pozostają zachowane.

Aktualizacja istniejącego wdrożenia po wgraniu zmienionych źródeł:

```bash
cd /home/PI26MSobol/pi26msobol.pythonanywhere.com
source /home/PI26MSobol/.virtualenvs/pi26msobol.pythonanywhere.com/bin/activate
python manage.py check
python manage.py migrate
python manage.py collectstatic --noinput
```

Następnie Web → Reload. Mapowanie static: `/static/` →
`/home/PI26MSobol/pi26msobol.pythonanywhere.com/staticfiles`.

Do niezależnego wdrożenia tego podkatalogu z GitHub użyj własnego virtualenv,
`pip install -r requirements.txt`, `migrate`, `collectstatic` oraz pliku WSGI:

```python
import os
import sys

sys.path.insert(0, '/home/PI26MSobol/myproject/lab4')
os.environ['DJANGO_SETTINGS_MODULE'] = 'lab4.settings'
os.environ['DJANGO_DEBUG'] = '0'
# Klucz ustaw tylko na serwerze, nie zapisuj go w GitHub.
os.environ['DJANGO_SECRET_KEY'] = 'TU_WSTAW_WLASNY_LOSOWY_KLUCZ'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Wygenerowanie klucza: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`.
W Web ustaw Source code na folder zawierający manage.py, virtualenv na używane
środowisko, a `/static/` na `staticfiles` tego projektu. Domena konta i localhost
są już w `ALLOWED_HOSTS`. Przy innej domenie zmień tę listę.

## Przepływ danych

Kliknięcie → fetch → views.books_api → ORM → SQLite → JSON → karty DOM.
Filtr `available=true/false` działa w bazie. Wygląd i funkcjonalność nie zostały zmienione.
