# Generated by Django 5.1.7 on 2025-04-09 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Paths', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Backgorund',
            new_name='Background',
        ),
        migrations.AlterUniqueTogether(
            name='point',
            unique_together={('order', 'path')},
        ),
    ]
