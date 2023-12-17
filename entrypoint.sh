#!/bin/bash
sudo nginx -g 'daemon on;'
gunicorn app.wsgi:application --bind "0.0.0.0:8000" --log-level debug --timeout 600 --worker-class=gevent --worker-connections=100 --workers=1