web: gunicorn hero.wsgi -b 0.0.0.0:8080 --log-file -
worker: celery -A hero worker -l info