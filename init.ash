#!/bin/ash

alembic upgrade head

pytest

python /app_dir/scripts/setup_initial_user.py

# gunicorn -b :8000 app.main:app --log-level DEBUG --enable-stdio-inheritance --workers 1 -k uvicorn.workers.UvicornWorker -t 600
gunicorn -b :8000 app.main:app --enable-stdio-inheritance --workers 1 -k uvicorn.workers.UvicornWorker -t 600