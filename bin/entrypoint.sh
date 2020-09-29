#!/usr/bin/env bash

# Create DB
flask db init
flask db migrate
flask db upgrade
flask seed_db -i seed.json

# Start app
flask run -h 0.0.0.0
