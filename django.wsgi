import os
import sys
sys.path = ['/var/test_aideco'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'aideco.settings'
import django.core.handlers.wsgi as wsgi_
application = wsgi_.WSGIHandler()