import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'fanmarkers.settings'
os.environ['MPLCONFIGDIR'] = '/var/cache/mpl'

import sys
sys.path = ['/srv/', '/srv/fanmarkers/'] + sys.path

import site
from settings_local import ENV_DIR
site.addsitedir(ENV_DIR + "/lib/python2.6/site-packages")

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()
