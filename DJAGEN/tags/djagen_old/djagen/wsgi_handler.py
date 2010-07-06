import sys
import os

# WSGI handler module.

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'djagen.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()