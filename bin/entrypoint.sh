#!/usr/bin/env bash

# Create DB
flask db init
flask db migrate
flask db upgrade
flask seed_db -i seed.json

# Start worker
rq worker default -u redis://redis:6379/0 &

# Start app
flask run -h 0.0.0.0
