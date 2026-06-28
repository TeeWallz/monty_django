#!/bin/sh
set -e
python manage.py migrate --noinput
exec gunicorn --worker-tmp-dir /dev/shm --no-control-socket monty_project.wsgi:application --bind 0.0.0.0:8000
