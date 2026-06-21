"""Settings de producción.

DEBUG queda en False y se activan las protecciones de seguridad.
ALLOWED_HOSTS y SECRET_KEY deben venir SIEMPRE de variables de entorno reales.
"""
from .base import *  # noqa: F401,F403

DEBUG = False

# HTTPS y cookies seguras
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
# Necesario detrás de un proxy/Render que termina el TLS.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# WhiteNoise con compresión y manifiesto para estáticos en producción.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
