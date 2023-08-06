SITE_ID = 1
STATIC_URL = '/static/'
ROOT_URLCONF = 'demoproject.urls'
SECRET_KEY = ';klkj;okj;lkn;lklj;lkj;kjmlliuewhy2ioqwjdkh'
ALLOWED_HOSTS = ('127.0.0.1',)
PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'crashlog',
        'HOST': '127.0.0.1',
        'PORT': '',
        'USER': 'postgres',
        'PASSWORD': ''
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'admin_extra_urls',
    'crashlog',
)


MIDDLEWARE = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'crashlog.middleware.CrashLogMiddleware',
)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)-8s: %(asctime)s %(name)10s: %(funcName)40s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'DEBUG'
        },
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': ['django.contrib.messages.context_processors.messages',
                                   'django.contrib.auth.context_processors.auth',
                                   "django.template.context_processors.request",
                                   ]
        },
    },
]
