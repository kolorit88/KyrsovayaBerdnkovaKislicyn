#!/bin/sh
set -e

# Ожидание PostgreSQL
echo "Waiting for PostgreSQL..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "PostgreSQL started"

# Ожидание Redis
echo "Waiting for Redis..."
while ! nc -z $REDIS_HOST $REDIS_PORT; do
  sleep 1
done
echo "Redis started"

# Применяем миграции Alembic
alembic upgrade head

# Запускаем приложение
exec uvicorn backend.main:app --host 0.0.0.0 --port 8000