import os

# Django settings for epicstudy project.

PROJECT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': './database/sqlite3.db', #'./database/sqlite3.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

#DATABASES = {
#  'default': {
#    'ENGINE': 'django.db.backends.postgresql_psycopg2',
#    'NAME': 'da2fp6udslmduv',
#    'HOST': 'ec2-107-22-165-77.compute-1.amazonaws.com',
#    'PORT': 5432,
#    'USER': 'bhxqskwurbjkgd',
#    'PASSWORD': '4C4fIzy2L97cr9BqAyejc8B37Z'
#  }
#}
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#STATIC_ROOT = os.path.join(PROJECT_PATH, 'static')
STATIC_ROOT = 'static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
#STATIC_URL = 'https://s3.amazonaws.com/epicstudy/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #os.path.join(PROJECT_PATH, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '^c90er&amp;vffwb3n--=%(@&amp;^kc+2sk$788^_ms*@9syqo(ark7do'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'audiofield.middleware.threadlocals.ThreadLocals',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Frontend widget values
CHANNEL_TYPE_VALUE = 0  # 0-Keep original, 1-Mono, 2-Stereo

FREQ_TYPE_VALUE = 8000  # 0-Keep original, 8000-8000Hz, 16000-16000Hz, 22050-22050Hz,
                     # 44100-44100Hz, 48000-48000Hz, 96000-96000Hz

CONVERT_TYPE_VALUE = 0 # 0-Keep original, 1-Convert to MP3, 2-Convert to WAV, 3-Convert to OGG

ROOT_URLCONF = 'epicstudy.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'epicstudy.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    './mytemplates',
    os.path.join(PROJECT_PATH, 'mytemplates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'flashcardapp',
    'social_auth',
    'videothumbs',
    'audiofield',
    'dajaxice',
    'haystack',
    'storages',
    'south'
)

#Values needed to connect to Amazon S3
#Stored as config variables on Heroku
#if 'AWS_ACCESS_KEY_ID' in os.environ:
    #AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
#if 'AWS_SECRET_ACCESS_KEY' in os.environ:
    #AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
#if 'S3_BUCKET_NAME' in os.environ:
    #AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET_NAME']


#STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
#DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

HAYSTACK_SITECONF = 'flashcardapp.search_sites'
HAYSTACK_SEARCH_ENGINE = 'simple'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
    'social_auth.backends.google.GoogleBackend',
)


LOGIN_URL           = '/login/google/'
LOGIN_REDIRECT_URL  = '/epicstudy'
LOGIN_ERROR_URL     = '/login-error/'


#TODO Setup proper redirect urls
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/epicstudy/'
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/epicstudy/newuserlogin/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/epicstudy/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/epicstudy/'
SOCIAL_AUTH_BACKEND_ERROR_URL = '/new-error-url/'
SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

TEMPLATE_CONTEXT_PROCESSORS = (
    'social_auth.context_processors.social_auth_by_name_backends',
    'social_auth.context_processors.social_auth_backends',
    'social_auth.context_processors.social_auth_by_type_backends',
    'django.contrib.auth.context_processors.auth',
)


SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UUID_LENGTH = 16
SOCIAL_AUTH_EXTRA_DATA = False
SOCIAL_AUTH_EXPIRATION = 'expires'
SOCIAL_AUTH_SESSION_EXPIRATION = False


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },    
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter':'verbose'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'dajaxice': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
            },        
    }
}

#import dj_database_url
#DATABASES['default'] =  dj_database_url.config()
