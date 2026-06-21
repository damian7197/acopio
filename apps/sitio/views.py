from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "sitio/home.html"


class ServiciosView(TemplateView):
    template_name = "sitio/servicios.html"


class NosotrosView(TemplateView):
    template_name = "sitio/nosotros.html"


class ContactoView(TemplateView):
    template_name = "sitio/contacto.html"