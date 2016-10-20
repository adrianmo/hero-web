FROM python:3.5

RUN apt-get update &&\
    apt-get install libmysqlclient-dev

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN pip install -r requirements.txt

RUN python3 manage.py migrate --no-input &&\
    python3 manage.py collectstatic --no-input

EXPOSE 8080

ENV DJANGO_CONFIGURATION=Prod

CMD ["gunicorn", "hero.wsgi", "-b", "0.0.0.0:8080", "--log-file", "-"]
