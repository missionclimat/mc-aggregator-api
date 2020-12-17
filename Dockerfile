FROM python:3.8 as django-dev

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./etc/requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /src/aggregator/

COPY ./aggregator/ .

CMD exec python manage.py runserver 0.0.0.0:8000

FROM django-dev as django

RUN python -m pip install gunicorn

WORKDIR /src/aggregator/

COPY /etc/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT [ "/usr/local/bin/docker-entrypoint.sh" ]

CMD exec gunicorn aggregator.wsgi --bind :8000
