from config.settings.base import *

DEBUG = False
ALLOWED_HOSTS = [
    'iratein.vercel.app',
    'www.iratein.vercel.app',
]

# *****  MEDIA FILES SETTINGS *****
# MEDIA_ROOT = '/home/iratein/cyber-security.iratein.com/media/'

CORS_ALLOWED_ORIGINS = [
    'https://iratein.vercel.app',
]

CSRF_TRUSTED_ORIGINS = [
    'https://iratein.vercel.app',
]

# HTTP verbs that are allowed
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "PATCH",
    "POST",
    "PUT",
]

# Whether to append trailing slashes to URLs.
APPEND_SLASH = True


'''  Deployment Security Configurations  '''

# *********************  CSRF PROTECTION  **********************************
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True


# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_SECONDS = '86400'
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_REFERRER_POLICY = 'origin-when-cross-origin'
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
