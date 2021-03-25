# This file is part of HappySchool.
#
# HappySchool is the legal property of its developers, whose names
# can be found in the AUTHORS file distributed with this source
# distribution.
#
# HappySchool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HappySchool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with HappySchool.  If not, see <http://www.gnu.org/licenses/>.

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')$g)mysea$a+_^mbzx$@!4lv_h$ecp@pp7a9g=%5ume#is6cg!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'channels',
    #'social_django',
    # "django_cas_ng",
    'crispy_forms',
    'core',
    'webpack_loader',
    'annuaire',
    'infirmerie',
    'appels',
    # 'absence_prof',
    'dossier_eleve',
    # 'mail_notification',
    # 'mail_answer',
    # 'schedule_change',
    # 'student_absence',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # "django_cas_ng.middleware.CASMiddleware",
]

if DEBUG:
    MIDDLEWARE.append('student_absence.middleware.SWHeaderMiddleware')


ROOT_URLCONF = 'happyschool.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.installed_apps.installed_apps',
                #'social_django.context_processors.backends',
                #'social_django.context_processors.login_redirect',
            ],
        },
    },
]

# Max size for uploaded file.
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME", "happyschool"),
        'USER': os.getenv("DB_USER", "happyschool"),
        'PASSWORD': os.getenv("DB_PASSWORD", "libreschool"),
        'HOST': os.getenv("DB_HOST", "localhost"),
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    # 'django_auth_ldap.backend.LDAPBackend', # For LDAP/ActiveDirectory authentification.
    # 'social_core.backends.google.GoogleOAuth2', # For google authentification.
    # 'social_core.backends.microsoft.MicrosoftOAuth2', # For microsoft authentification.
    # "django_cas_ng.backends.CASBackend", # For SSO with a CAS server.
]

if 'social_django' in INSTALLED_APPS:
    SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.auth_allowed',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.user.get_username',
        # 'social_core.pipeline.mail.mail_validation',
        'social_core.pipeline.social_auth.associate_by_email',
        # 'social_core.pipeline.user.create_user',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
    )

SOCIAL_AUTH_POSTGRES_JSONFIELD = True
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'key'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'secret'

# An key/secret must be created in
# https://portal.azure.com/ > Azure Active Directory > Application registration
# and a redirect url must be added, https is mandatory.
SOCIAL_AUTH_MICROSOFT_GRAPH_KEY = "keyyy-keyyyy-keyyyy"
SOCIAL_AUTH_MICROSOFT_GRAPH_SECRET = "the_secret"
SOCIAL_AUTH_MICROSOFT_GRAPH_REDIRECT_URL = "https://MYBASEURL/complete/microsoft-graph"

SOCIAL_AUTH_REDIRECT_IS_HTTPS = False

CAS_SERVER_URL = "https://example.com/cas/"
CAS_CREATE_USER = False

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

if DEBUG:
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static/"),
        'static/',
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

CRISPY_TEMPLATE_PACK = 'bootstrap3'

LOGIN_URL = 'auth'
LOGIN_REDIRECT_URL = 'annuaire'

# Mostly use in debug mode to reroute emails.
EMAIL_ADMIN = os.getenv("EMAIL_ADMIN", "")

EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.server.com")
EMAIL_PORT = os.getenv("EMAIL_PORT", 465)
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "admin@example.org")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "password")
EMAIL_FROM = os.getenv("EMAIL_FROM", "robot@example.org")

if EMAIL_PORT == 465:
    EMAIL_USE_SSL = True
elif EMAIL_PORT == 587:
    EMAIL_USE_TLS = True

# Group mapping
SYSADMIN_GROUP = "sysadmin"
DIRECTION_GROUP = "direction"
TEACHER_GROUP = "professeur"
EDUCATOR_GROUP = "educateur"
COORDONATOR_GROUP = "coordonateur"
SECRETARY_GROUP = "secretaire"
PMS_GROUP = "pms"
RECEPTION_GROUP = "accueil"
COORD_GROUP = "coord"
EDUC_GROUP = "educ"

USE_LDAP_INFO = False

LDAP_HOST = os.getenv("LDAP_HOST", "localhost")
LDAP_DOMAIN = os.getenv("LDAP_DOMAIN", "dc=example,dc=org")

# Use LDAP to authenticate
USE_LDAP_AUTH = False
if USE_LDAP_AUTH:
    AUTH_LDAP_BIND_AS_AUTHENTICATING_USER = True
    AUTH_LDAP_BIND_DN = os.getenv("LDAP_USER", "cn=admin,dc=example,dc=org")
    AUTH_LDAP_BIND_PASSWORD = os.getenv("LDAP_PWD", "ldap_password")
    AUTH_LDAP_SERVER_URI = "ldap://" + LDAP_HOST
    if AUTH_LDAP_BIND_AS_AUTHENTICATING_USER:
        AUTHENTICATION_BACKENDS.append('django_auth_ldap.backend.LDAPBackend')

if USE_LDAP_INFO:
    import ldap
    from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
    AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=people,%s" % LDAP_DOMAIN,
                                       ldap.SCOPE_SUBTREE, "(uid=%(user)s)")

    AUTH_LDAP_USER_ATTR_MAP = {"first_name": "cn", "last_name": "sn", "username": "uid",
                           "password": "userPassword"}

    groups = [SYSADMIN_GROUP, DIRECTION_GROUP, TEACHER_GROUP, EDUCATOR_GROUP, SECRETARY_GROUP, PMS_GROUP, RECEPTION_GROUP]
    active_groups = map(lambda g: "cn=%s,ou=groups,%s" % (g, LDAP_DOMAIN), groups)

    AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        "is_active": list(active_groups),
        "is_staff": "cn=sysadmin,ou=groups,%s" % LDAP_DOMAIN,
        "is_superuser": "cn=sysadmin,ou=groups,%s" % LDAP_DOMAIN
    }

    AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=groups,%s" % LDAP_DOMAIN,
                                        ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
                                    )
    AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")
    AUTH_LDAP_FIND_GROUP_PERMS = True
    AUTH_LDAP_MIRROR_GROUPS = True

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'fr-be'

TIME_ZONE = 'Europe/Brussels'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_INPUT_FORMATS = [
    '%H:%M:%S',     # '14:30:59'
    '%H:%M:%S.%f',  # '14:30:59.000200'
    '%H:%M',        # '14:30'
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

CELERY_NAME = "happyschool"
CELERY_BACKEND = "redis"
CELERY_BROKER = 'redis://localhost:6379'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE


ASGI_APPLICATION = "happyschool.routing.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}

MAILGUN_KEY = "your-mailgun-key"
SPARKPOST_KEY = "your-sparkpost-key"

EMAIL_ATTACHMENTS_SYNC = {
    'rsync_command': "/usr/bin/rsync -e ssh -avz --delete-after /home/user/happyschool/media/mail_notification happyschool@remote:/home/user/happyschool/media",
}


# The following setting allows to sync db (templates and mail answers) from local to remote server. It uses an ssh connection and pg_dump to
# transfer the data through an unix pipe. Please change the related db settings as well as the ssh user and server.
MAIL_ANSWER = {
    'template_sync': """PGPASSWORD=local_pwd pg_dump -h localhost -U db_user -d db_name -O --column-inserts --clean \
        -t mail_answer_optionmodel\
        -t mail_answer_choicemodel\
        -t mail_answer_mailtemplatemodel\
        -t mail_answer_mailtemplatemodel_choices\
        -t mail_answer_mailtemplatemodel_options\
    | ssh happyschool@remote 'PGPASSWORD=remote_pwd psql -h localhost -U "db_user" -d "db_name"'""",
    'mail_answers_create' : """PGPASSWORD=local_pwd pg_dump -h localhost -U db_user -d db_name -O --column-inserts -a \
        -t mail_answer_mailanswermodel\
    | ssh happyschool@remote 'PGPASSWORD=remote_pwd psql -h localhost -U "db_user" -d "db_name"'"""
}

# Use synchronization capabilities with one or multiple ProEco databases. Need libreschoolfdb python package.
SYNC_FDB = False
if SYNC_FDB:
    # The corresponding teaching need to be created before trying to synchronize.
    from libreschoolfdb import fdbserver
    SYNC_FDB_SERVER = [
        {
            # The custom name field of the teaching model.
            "teaching_name": "etablissement_technique",
            # The way the data are stored in ProEco (secondaire or primaire).
            "teaching_type": "secondaire",
            # Access configuration to the ProEco database.
            "server": fdbserver.FDBServer(host="192.168.1.1", path='C:/ProEco/DataFB/',
                                          user='complex_login', password='complex_pwd'),
            # Classe format.
            "classe_format": "%C",
            # A mapping of a unique attribute shared between ProEco and a LDAP server.
            "ldap_unique_attr": {
                "teacher_ldap_attr":"id", # Attribute from the LDAP server for teachers.
                "student_ldap_attr": "matricule", # Attribute from the LDAP server for students.
                "teacher_model_attr": "matricule", # Attribute from ResponsibleModel (matricule, email,…).
                "student_model_attr": "matricule", # Attribute from StudentModel (matricule,…).
            }
        }
    ]
