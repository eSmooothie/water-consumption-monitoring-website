web: gunicorn water_consumption_site.wsgi --log-file - --keep-alive 5 --log-level debug
release: python manage.py migrate
