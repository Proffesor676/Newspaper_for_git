
from pathlib import Path
import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-c!*hy0ha=llr%+3p%j3a*^q1by(=rnzt0+96&5t8z7gby*x8@)'

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news.apps.NewsConfig',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_filters',
    'accounts',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    "django_apscheduler",
    'celery',

]
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
]

ROOT_URLCONF = 'newspaper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'newspaper.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

LOGIN_REDIRECT_URL = "/posts"  #Ссылка куда перенаправляешься после входа в профиль

AUTHENTICATION_BACKENDS = [           #Разделы для allauth
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}

SITE_URL = "http://127.0.0.1:8000"

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = "Professor676"
EMAIL_HOST_PASSWORD = "botngpqzurynreeu"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = "Professor676@yandex.by"

APSCHEDULER_DATETIME_FORMAT = 'N j, Y, f:s a'

APSCHEDULER_RUN_NOW_TIMEOUT = 25

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
    }
}

# Создаём логгер
logger = logging.getLogger('django')
logger.setLevel(logging.DEBUG)

# функция отправки письма с логами ERRORS и выше
def send_email_for_errors_and_above(record):
    if record.levelno >= logging.ERROR and record.name in ['django.request', 'django.server']:
        send_logs_email()

# создаём консоль хэндлер
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# создаём фильтр и добавляем его в хэндлер
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# создаём файл с сообщениями general
file_handler = logging.FileHandler('general.log')
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# создаём консоль хэндлер
if DEBUG == True:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
else:
    # создаём хэндлер с сообщениями логов INFO и выше
    file_handler = logging.FileHandler('general.log')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    # добавляем функцию отправки письма
    logger.addFilter(send_email_for_errors_and_above)

# создаём файл errors
error_handler = logging.FileHandler('errors.log')
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(pathname)s\n%(exc_info)s')
error_handler.setFormatter(error_formatter)
logger.addHandler(error_handler)

# создаём файл security
security_handler = logging.FileHandler('security.log')
security_handler.setLevel(logging.DEBUG)
security_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
security_handler.setFormatter(security_formatter)
security_handler.addFilter(logging.Filter('django.security'))
logger.addHandler(security_handler)


# создаём функцию для отправки сообщений
def send_logs_email():
    # устанавливаем параметры письма
    sender_email = 'sender@example.com'
    receiver_email = 'receiver@example.com'
    subject = 'Django Logs'

    # создаём объект сообщения
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Текст сообщения
    body = 'Сообщения из Djngo логи'
    message.attach(MIMEText(body, 'plain'))

    # прикрепляем лог файлы к сообщению
    for filename in ['errors.log', 'django.request.log', 'django.server.log']:
        with open(filename, 'rb') as file:
            attachment = MIMEApplication(file.read(), _subtype='txt')
            attachment.add_header('Content-Disposition', 'attachment', filename=filename)
            message.attach(attachment)

    # отправка сообщения
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, 'password')
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        logger.info('Email sent with logs.')
    except Exception as e:
        logger.error(f'Error sending email: {e}')

# добавляем функцию в логгер как фильтр
logger.addFilter(send_email_for_errors_and_above)