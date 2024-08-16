"""
WSGI config for crudexample project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""


import os
import sys

path = '/home/sunilc/CRUD/crudexample'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'crudexample.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
