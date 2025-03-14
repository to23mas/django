from django.db import models

class Habit(models.Model):
    name = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    date_completed = models.DateField(null=True, blank=True)
    completion_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category, related_name='posts')

    def __str__(self):
        return self.title
