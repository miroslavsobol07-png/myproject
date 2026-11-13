from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'year', 'genre', 'available', 'rating', 'added_on']
    list_filter = ['available', 'genre', 'rating']
    list_editable = ['available', 'rating']
    search_fields = ['title', 'author']
    date_hierarchy = 'added_on'
