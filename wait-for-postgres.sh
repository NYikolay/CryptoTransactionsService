#!/bin/bash

until PGPASSWORD=$POSTGRES_PASSWORD psql -h $POSTGRES_HOST -U $POSTGRES_USER -c '\q'; do
  echo "PostgreSQL не доступен. Повторная попытка через 2 секунды..."
  sleep 1
done

python manage.py runserver