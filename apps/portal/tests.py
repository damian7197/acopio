import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.portal.models import Cliente, Movimiento

User = get_user_model()


class AislamientoTests(TestCase):
    """El test más importante del portal: un cliente NUNCA ve datos de otro."""

    def setUp(self):
        # Cliente A: soja, 1000 kg
        self.user_a = User.objects.create_user(username="1001", password="clave-a")
        self.cliente_a = Cliente.objects.create(
            numero_cliente="1001", nombre="Cliente A", user=self.user_a
        )
        Movimiento.objects.create(
            cliente=self.cliente_a, fecha=datetime.date(2025, 3, 1),
            cosecha="2024/25", especie="soja", tipo="ingreso", kilos=1000,
        )

        # Cliente B: maiz, 5000 kg
        self.user_b = User.objects.create_user(username="2002", password="clave-b")
        self.cliente_b = Cliente.objects.create(
            numero_cliente="2002", nombre="Cliente B", user=self.user_b
        )
        Movimiento.objects.create(
            cliente=self.cliente_b, fecha=datetime.date(2025, 3, 2),
            cosecha="2024/25", especie="maiz", tipo="ingreso", kilos=5000,
        )

    def test_anonimo_es_redirigido_al_login(self):
        resp = self.client.get(reverse("portal:resumen"))
        self.assertEqual(resp.status_code, 302)

    def test_cliente_solo_ve_lo_suyo(self):
        self.client.login(username="1001", password="clave-a")
        resp = self.client.get(reverse("portal:resumen"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "soja")       # lo propio SÍ aparece
        self.assertNotContains(resp, "maiz")     # lo del otro NO
        self.assertNotContains(resp, "5000")     # los kilos del otro tampoco
