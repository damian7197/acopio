from django.test import TestCase
from django.urls import reverse


class SitioPagesTests(TestCase):
    def test_paginas_responden_ok(self):
        for nombre in ["home", "servicios", "nosotros", "contacto"]:
            with self.subTest(pagina=nombre):
                resp = self.client.get(reverse(f"sitio:{nombre}"))
                self.assertEqual(resp.status_code, 200)