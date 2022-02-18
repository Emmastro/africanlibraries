import os

from django.core.wsgi import get_wsgi_application


DEBUG = False
	
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Connect to production database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'africanlibraries',
        'USER': 'emmamurairi',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Use the statics and media from Amazon

#from .amazon_files import *

#--allow-unrelated-histories
# Security settings ** Set after getting the SSL certificate

CORS_REPLACE_HTTPS_REFERER      = False
HOST_SCHEME                     = "http://"
SECURE_PROXY_SSL_HEADER         = None
SECURE_SSL_REDIRECT             = False
SESSION_COOKIE_SECURE           = False
CSRF_COOKIE_SECURE              = False
SECURE_HSTS_SECONDS             = False
SECURE_HSTS_INCLUDE_SUBDOMAINS  = False
SECURE_FRAME_DENY               = False
