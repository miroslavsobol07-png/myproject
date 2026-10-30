from django.db import models


class Book(models.Model):
    # Sześć pól opisuje książkę; Django dodaje też identyfikator id.
    title = models.CharField('tytuł', max_length=150)
    author = models.CharField('autor', max_length=100)
    description = models.TextField('opis')
    year = models.PositiveIntegerField('rok wydania')
    genre = models.CharField('gatunek', max_length=60)
    available = models.BooleanField('dostępna', default=True)

    class Meta:
        ordering = ['title', 'id']
        verbose_name = 'książka'
        verbose_name_plural = 'książki'

    def __str__(self):
        return f'{self.title} – {self.author}'
