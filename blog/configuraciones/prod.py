from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['matiassosadev.pythonanywhere.com']

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '$h2mfmn-h@isio!v%pbr5i710_k&(&uyui%#$8z5)0^ksoz$^%')

STATIC_ROOT = os.path.join(BASE_DIR.parent, 'staticfiles')

MEDIA_ROOT = os.path.join(BASE_DIR.parent, 'mediafiles')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR.parent / 'db.sqlite3',
    }
}