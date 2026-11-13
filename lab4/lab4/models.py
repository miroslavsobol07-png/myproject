from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Book(models.Model):
    # Pola z laboratorium 4 pozostają bez zmian.
    title = models.CharField('tytuł', max_length=150)
    author = models.CharField('autor', max_length=100)
    description = models.TextField('opis')
    year = models.PositiveIntegerField('rok wydania')
    genre = models.CharField('gatunek', max_length=60)
    available = models.BooleanField('dostępna', default=True)
    # Puste wartości pozwalają zachować książki dodane przed laboratorium 5.
    rating = models.PositiveSmallIntegerField(
        'ocena', null=True, blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Ocena od 1 do 5. Można pozostawić puste.',
    )
    added_on = models.DateField('data dodania do biblioteki', null=True, blank=True)

    class Meta:
        ordering = ['title', 'id']
        verbose_name = 'książka'
        verbose_name_plural = 'książki'

    def __str__(self):
        return f'{self.title} – {self.author}'
