web:python manage.py runserver
web: gunicorn FoodPlanner.wsgi --timeout 60 --keep-alive 5 --log-level debug
heroku ps:scale web=1