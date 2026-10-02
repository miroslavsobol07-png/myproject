from datetime import datetime
from zoneinfo import ZoneInfo

from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return HttpResponse("Witaj w Django!")


def hello_name(request, name):
    return HttpResponse(f"Witaj, {name}!", content_type="text/plain; charset=utf-8")


def hello_template(request, name):
    return render(request, "witaj/hello.html", {"name": name})


def current_time(request):
    now = datetime.now(ZoneInfo("Europe/Warsaw"))
    return render(request, "witaj/time.html", {"now": now.strftime("%d.%m.%Y, godzina: %H:%M")})
