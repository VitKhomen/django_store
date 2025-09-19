#!/bin/sh

set -e  # если ошибка — сразу стоп

echo "👉 Running migrations..."
python manage.py migrate --noinput

echo "👉 Creating superuser (if not exists)..."
python manage.py createsu

echo "👉 Collecting static files..."
python manage.py collectstatic --noinput

echo "👉 Starting Gunicorn..."
gunicorn django_store.wsgi:application --bind 0.0.0.0:$PORT