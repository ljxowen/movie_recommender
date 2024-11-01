#! /usr/bin/env bash

# Let the DB start
python /app/app/backend_pre_start.py

#only used when first time start the backend, init first migration version of database
#alembic revision --autogenerate -m "init model"

# Run migrations
alembic upgrade head

# Create initial data in DB
python /app/app/initial_data.py