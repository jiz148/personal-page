# Generated by Django 3.1.4 on 2020-12-27 15:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20201227_2308'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='article',
            name='favorites',
        ),
        migrations.RemoveField(
            model_name='article',
            name='owner',
        ),
    ]