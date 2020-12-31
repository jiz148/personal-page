#!/bin/bash
python manage.py makemigrations&&
python manage.py migrate&&
uwsgi --ini /var/www/html/personal-page/uwsgi.ini
# python manage.py runserver 0.0.0.0:8000
