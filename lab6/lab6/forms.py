from django import forms
from lab4.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'year', 'genre',
                  'available', 'rating', 'added_on']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'year': forms.NumberInput(attrs={'min': 1, 'max': 9999}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'added_on': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_year(self):
        year = self.cleaned_data['year']
        if not 1 <= year <= 9999:
            raise forms.ValidationError('Podaj rok od 1 do 9999.')
        return year
