from django.test import TestCase
from django.urls import reverse

class PaymentsTests(TestCase):
    def test_pricing_page(self):
        r = self.client.get(reverse("payments:pricing"))
        self.assertEqual(r.status_code, 200)
