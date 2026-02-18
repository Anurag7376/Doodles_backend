#!/bin/sh

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
