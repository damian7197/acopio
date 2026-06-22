from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import LoginClienteForm

app_name = "portal"

urlpatterns = [
    path("", views.resumen, name="resumen"),
    path(
        "ingresar/",
        auth_views.LoginView.as_view(
            template_name="portal/login.html",
            authentication_form=LoginClienteForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("salir/", auth_views.LogoutView.as_view(), name="logout"),
]
