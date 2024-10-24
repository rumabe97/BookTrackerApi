import uuid

from django.db import models


# Create your models here.

class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idGoogle = models.CharField(editable=False, max_length=255)
    STATUS_CHOICES = [
        ('reading', 'Reading'),
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('wishlist', 'Wishlist'),
    ]
    title = models.CharField(max_length=255, unique=True, null=False, default='')
    subTitle = models.CharField(max_length=255, unique=False, null=True, default='')
    description = models.CharField(max_length=10000, unique=False, null=True, default='')
    author = models.CharField(max_length=255, default="Anonymous")
    genre = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    pages = models.PositiveIntegerField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    averageRating = models.PositiveSmallIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    coverImage = models.URLField(max_length=500, blank=True, null=True)
    publishedDate = models.DateTimeField(null=True, blank=True)
    isbn13 = models.CharField(max_length=13, unique=True, null=True, blank=True)
    isbn10 = models.CharField(max_length=10, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title']
        constraints = [
            models.CheckConstraint(check=models.Q(averageRating__gte=0, averageRating__lte=5),
                                   name='average_rating_range'),
            models.CheckConstraint(check=models.Q(rating__gte=0, rating__lte=5), name='rating_range')
        ]

    def __str__(self):
        return self.title

        class Meta:
            ordering = ['-id']
