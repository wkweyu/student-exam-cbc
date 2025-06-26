AUTH_USER_MODEL = 'users.CustomUser'

INSTALLED_APPS = [
    ...
    'rest_framework',
    'corsheaders',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'users',
    'users',
    'students',
    'subjects',
    'exams',
    'grading',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

CORS_ORIGIN_ALLOW_ALL = True  # or configure specific origins
