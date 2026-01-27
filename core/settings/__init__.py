from decouple import config

DJANGO_ENV = config('DJANGO_ENV')  # .env fayldan oladi

if DJANGO_ENV == 'development':
    from .development import *
elif DJANGO_ENV == 'production':
    from .production import *
else:
    raise Exception('DJANGO_ENV is not installed or unknown.')
