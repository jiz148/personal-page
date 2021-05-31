#!/bin/bash
python manage.py collectstatic --noinput&&
python manage.py makemigrations&&
python manage.py migrate&&
# python manage.py runserver 0.0.0.0:8000
uwsgi --ini /var/www/html/personal-page/uwsgi.ini
tail -f /dev/null

exec "$@"
