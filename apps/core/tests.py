from django.test import TestCase


class HomePageTests(TestCase):
    def test_home_responde_ok(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
