#!/bin/bash
export FLASK_APP=app.py
export FLASK_DEBUG=true
export FLASK_ENV=development
gunicorn --certfile=certs/smart-ramp-dev.crt --keyfile=certs/smart-ramp-dev.key --bind 0.0.0.0:443 app:app --preload --workers=2 --access-logfile /var/log/flask-ramp/gunicorn-access.log --error-logfile /var/log/flask-ramp/gunicorn-error.log 