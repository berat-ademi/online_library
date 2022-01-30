import environ

from app.settings.base import *

env = environ.ENV(
    DEBUG=(bool, False)
)

# False if not in os.environ
DEBUG = env('DEBUG')

# Raises django`s ImproperlyConfigured exeption if SECRE_KEY not in  os.environ
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


# Parse database connection url strings like psql://user:pass@127.0.0.1:8458/db
DATABASES = {
    # read os.environ['DATABASES_URL'] and raises ImproperlyConfigured exeption if
    'default': env.db(),
}