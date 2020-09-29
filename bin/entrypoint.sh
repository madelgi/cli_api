#!/usr/bin/env bash

# Initialize database
flask db init
flask db migrate
flask db upgrade

# Start app
flask run -h 0.0.0.0
