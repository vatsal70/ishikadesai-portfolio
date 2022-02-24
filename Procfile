web: gunicorn portfolio.wsgi --log-file - 
worker: celery -A portfolio worker -l info -B