#!/bin/bach

alembic upgrade head

gunicorn app.main:app --workers 4 --worker-class unicorn.workers.UvicornWorker --bind=0.0.0.0:8000