from django.db import models


# Create your models here.
class Author(models.Model):
    # an Author model with the name field
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    # a Book model with title, author (ForeignKey to Author), and publication_year fields
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    publication_year = models.IntegerField()

    def __str__(self):
        return self.title
