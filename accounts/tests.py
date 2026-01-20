from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()

class AccountsTests(TestCase):
    def test_signup_creates_profile(self):
        r = self.client.post(reverse("accounts:signup"), {
            "username": "me",
            "email": "me@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        })
        self.assertIn(r.status_code, (200, 302))
        u = User.objects.get(username="me")
        self.assertTrue(hasattr(u, "profile"))

    def test_login_page_anonymous_only(self):
        u = User.objects.create_user(username="x", password="StrongPass123!")
        self.client.login(username="x", password="StrongPass123!")
        r = self.client.get(reverse("accounts:login"))
        self.assertEqual(r.status_code, 302)
