#!/bin/bash

# Start Redis server in the background
redis-server &

# Start the Flask application
python3 app.py
