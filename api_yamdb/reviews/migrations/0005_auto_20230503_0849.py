# Generated by Django 3.2 on 2023-05-03 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_merge_20230503_0849'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='rating',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
