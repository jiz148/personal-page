# Generated by Django 3.1.4 on 2020-12-27 06:00

import blog.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='picture',
            field=blog.fields.RestrictedFileField(upload_to='article_pic'),
        ),
    ]