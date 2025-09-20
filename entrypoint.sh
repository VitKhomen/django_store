#!/bin/sh
set -e

echo "👉 Running user migrations first..."
python manage.py migrate users --noinput

echo "👉 Running all other migrations..."
python manage.py migrate --noinput

echo "👉 Creating superuser (if not exists)..."
python manage.py createsu

echo "👉 Collecting static files..."
python manage.py collectstatic --noinput

echo "👉 Starting Gunicorn..."
gunicorn django_store.wsgi:application --bind 0.0.0.0:$PORT