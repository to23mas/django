# Generated by Django 5.0.2 on 2025-04-15 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='question_type',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
