from django.shortcuts import render

def index(request):
    return render(request, 'Lab_2/index.html')
