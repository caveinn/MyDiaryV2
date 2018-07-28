web: gunicorn --workers=1 run:app
release: createdb diary
release: python manage.py 
release: export APP_SETTINGS= "production"