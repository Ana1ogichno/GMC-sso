#!/usr/bin/env bash

scripts/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT
PYTHONPATH=. alembic upgrade head
alembic check
scripts/prestart.sh
python3 run.py