#!/bin/bash
PYTHONPATH=/opt/app/backend/src gunicorn main:app --bind $HOST:$PORT --reload