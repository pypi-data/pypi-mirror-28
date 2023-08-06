$ pip install django-simplefeedback

add 'simple-feedback' to INSTALLED_APPS

include 'simple-feedback.urls' into urlpatterns

Test standalone app:

$ export DATABASE_URL='your_db'  # you can skip this, defaults to 'localhost' (use postgres.app for simplicity)

$ pip install -r requirements.txt

$ python runtests.py
