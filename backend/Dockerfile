FROM python:3.10.12-slim AS base

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt -y update \
    && pip install --upgrade pip \
    && pip install poetry \
    && pip install greenlet \
    && pip install Flask-Limiter \
    && pip install marshmallow flask-marshmallow \
    && pip install -U Flask-SQLAlchemy \
    && pip install flask-cors \
    && pip install Flask-Caching \
    && pip install flask-wtf flasgger\
    && pip install python-dateutil \
    && pip install pytest pytest-mock factory_boy \
    && pip install flask-jwt-extended \
    && apt install -y libpq-dev gcc \
    && poetry config virtualenvs.create false

COPY ./entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
RUN mkdir backend
COPY ./backend/pyproject.toml /opt/app/backend
WORKDIR /opt/app/backend
RUN poetry install --no-interaction --no-ansi



FROM base

COPY . .

ENTRYPOINT ["entrypoint.sh"]