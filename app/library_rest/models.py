from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13)
    pages = models.IntegerField()
    published_date = models.DateField()

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'pages': self.pages,
            'published_date': str(self.published_date)
        }
