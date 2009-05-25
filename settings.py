# Django settings for jobmap project.
import os
#from googlemap.settings import *

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
TEMPLATE_DEBUG = DEBUG
AUTH_PROFILE_MODULE = 'main.profile'
STATIC_DOC_ROOT = '/home/nbv4/jobmap/media'
ACCOUNT_ACTIVATION_DAYS = 5
SECRET_KEY = "ABQIAAAAtDznsRv92g_KZ0HK9mBD5RS3ydai3R5pSwWU_IHTQxn79Z9awhQaWXs60I2yGfPRz5z-Bs_CTn5lMg"

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql_psycopg2'			#'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'jobmap'				#'nbv4_jobmap'             # Or path to database file if using sqlite3.
DATABASE_USER = 'chris'					#'nbv4_logbook'             # Not used with sqlite3.
DATABASE_PASSWORD = 'nbv4is'				#'D1E3T%4Y5^N7'         # Not used with sqlite3.
DATABASE_HOST = ''					# Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''					# Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/nbv4/jobmap/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ag5jl++k=23=(i+j=fya7e^fqr8cos4f!oass9s$&=s0)=0zj7'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'jobmap.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates')
)

INSTALLED_APPS = (
    'main',
    'django.contrib.comments',
    'django.contrib.admindocs',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.gis',
    'django.contrib.humanize',
    'registration',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    #'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'main.context_processors.titles',
    'main.context_processors.top_numbers',
)
