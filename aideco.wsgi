import os
import sys
sys.path.insert(0, '/var/test_aideco')
os.environ['DJANGO_SETTINGS_MODULE'] = 'aidco.settings'
import django.core.handlers.wsgi as wsgi_
application = wsgi_.WSGIHandler()