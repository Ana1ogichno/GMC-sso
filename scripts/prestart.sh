#! /usr/bin/env bash

# Let the DB start
python3 scripts/pre_start.py

### Create initial data in DB
python3 scripts/initial_data.py
