from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Segurança
SECRET_KEY = "django-insecure-xz+7hj!xyv6@#^%k6fl_yk%r5l(e-s%p^2a+7)%b-m&6r8wmjh"
DEBUG = True
ALLOWED_HOSTS = ['Dr1gues.pythonanywhere.com']

# Apps instaladas
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pessoas",
    "bandas",
    "artigos",
    "noobsite",
    "portfolio",
    "django_extensions",  # Adicionada no final
]

# django-extensions para gerar diagrama
GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'portfolio.middleware.ContadorVisitantesMiddleware',
]

ROOT_URLCONF = "project.urls"

# Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # ou adiciona Path para templates se necessário
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'portfolio.context_processors.total_visitantes',
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

# Base de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Dr1gues$default',
        'USER': 'Dr1gues',
        'PASSWORD': 'progweb2025',  # substitui pela tua password real
        'HOST': 'Dr1gues.mysql.pythonanywhere-services.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}


# Validação de senha
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internacionalização
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Ficheiros estáticos
STATIC_URL = '/static/'
STATIC_ROOT = '/home/Dr1gues/project/static'

# Ficheiros media (se necessário)
MEDIA_ROOT = '/home/Dr1gues/project/media'
MEDIA_URL = '/media/'

# ID default para modelos
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
