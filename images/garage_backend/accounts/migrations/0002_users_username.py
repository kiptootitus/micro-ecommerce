# Generated by Django 5.1.7 on 2025-03-22 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='username',
            field=models.CharField(default=True, max_length=255, unique=True),
        ),
    ]
