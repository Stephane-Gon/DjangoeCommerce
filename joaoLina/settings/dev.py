from .base import *

SECRET_KEY = "=)wt+1c4k)mlvlfc8e5(mm2l0_%v29j6@h#u@e2%03!bq(&b!"

DEBUG = True

ALLOWED_HOSTS = ['*']


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')