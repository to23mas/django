from django.db import models


class Birthday(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField()
    calendar_name = models.CharField(max_length=100, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['birth_date']
        unique_together = ['name', 'birth_date']
        verbose_name_plural = 'Birthdays'

    def __str__(self):
        return f"{self.name} ({self.birth_date.strftime('%d/%m/%Y')})"
