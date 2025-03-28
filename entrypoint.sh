#!/bin/bash
alembic upgrade head
PYTHONPATH=/opt/app/backend/src gunicorn main:app --bind $HOST:$PORT --reload