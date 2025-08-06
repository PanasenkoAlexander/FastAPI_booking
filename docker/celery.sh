#!/bin/bach

if [[ "${1}" == "celery" ]]; then
  celery --app=app.tasks.celery:celery worker -1 INFO
elif [[ "${1}" == "flower" ]]; then
  celery --app=app.tasks.celery:celery flower
fi
