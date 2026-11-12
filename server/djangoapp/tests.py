import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase


class AuthenticationEndpointTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="correct-horse-battery-staple"
        )
        self.client = Client(enforce_csrf_checks=True)
        csrf_response = self.client.get("/djangoapp/csrf")
        self.csrf_token = csrf_response.json()["csrfToken"]

    def test_login_and_logout_with_csrf_protection(self):
        login_response = self.client.post(
            "/djangoapp/login",
            data=json.dumps(
                {"userName": self.user.username, "password": "correct-horse-battery-staple"}
            ),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.json()["userName"], self.user.username)
        self.assertEqual(login_response.json()["status"], "Authenticated")

        logout_response = self.client.post(
            "/djangoapp/logout",
            HTTP_X_CSRFTOKEN=login_response.json()["csrfToken"],
        )

        self.assertEqual(logout_response.status_code, 200)
        self.assertEqual(logout_response.json(), {"userName": ""})
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_rejects_invalid_credentials(self):
        response = self.client.post(
            "/djangoapp/login",
            data=json.dumps({"userName": self.user.username, "password": "wrong"}),
            content_type="application/json",
            HTTP_X_CSRFTOKEN=self.csrf_token,
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"error": "Invalid username or password."})

    def test_login_requires_csrf_token(self):
        response = self.client.post(
            "/djangoapp/login",
            data=json.dumps(
                {"userName": self.user.username, "password": "correct-horse-battery-staple"}
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)

    def test_logout_requires_post(self):
        response = self.client.get("/djangoapp/logout")

        self.assertEqual(response.status_code, 405)
