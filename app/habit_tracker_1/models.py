from django.db import models

class Habit(models.Model):
    name = models.CharField(max_length=200)
    completed = models.BooleanField(default=False) # type: ignore
    date_completed = models.DateField(null=True, blank=True) # type: ignore
    completion_count = models.PositiveIntegerField(default=0) # type: ignore

    def __str__(self): # type: ignore
        return self.name

