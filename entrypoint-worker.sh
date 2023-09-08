#!/bin/sh

celery -A Tasker worker --loglevel=info --concurrency 1 -E
echo "Celery is configured successfully."
