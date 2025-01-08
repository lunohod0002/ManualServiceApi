#!/bin/bash
alembic upgrade head
python -m app.database.insert_data
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000
