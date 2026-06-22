from django.contrib.auth.forms import AuthenticationForm


class LoginClienteForm(AuthenticationForm):
    """Login estándar, pero con la etiqueta 'Número de cliente'."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Número de cliente"
