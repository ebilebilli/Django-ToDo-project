# Generated by Django 5.1.4 on 2025-01-15 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='conxtext',
        ),
        migrations.RemoveField(
            model_name='note',
            name='title',
        ),
        migrations.AddField(
            model_name='note',
            name='context',
            field=models.TextField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
