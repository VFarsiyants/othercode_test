#!/bin/sh

echo "Running migrations"
alembic upgrade head

# Install fixtures
echo "Install fixtures"
python loadfixtures.py

# start server
uvicorn src.main:app --host 0.0.0.0 --port 8000
