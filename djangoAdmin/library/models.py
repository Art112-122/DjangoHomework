from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=150)
    birth_year = models.PositiveIntegerField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    STATUS_CHOICES = (
        ("available", "Available"),
        ("borrowed", "Borrowed"),
        ("archived", "Archived"),
    )

    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    pages = models.PositiveIntegerField()
    published_year = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
