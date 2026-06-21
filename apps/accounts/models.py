from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Usuario custom del proyecto.

    Se define desde el inicio (antes de la primera migración) para poder
    extenderlo más adelante —por ejemplo, vinculándolo a un Cliente— sin
    el dolor de cambiar el modelo de usuario con datos ya cargados.
    """

    pass
