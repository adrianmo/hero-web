#!/usr/bin/env bash

echo "=> Applying database migrations"
python manage.py migrate

echo "=> Generating static files"
python3 manage.py collectstatic --noinput

echo "=> Starting server"
gunicorn hero.wsgi -b 0.0.0.0:8080 --log-file -
