#!/usr/bin/env bash

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
gunicorn hero.wsgi -b 0.0.0.0:8080 --log-file -
