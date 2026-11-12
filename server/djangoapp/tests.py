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


class DealerHomePageTests(TestCase):
    def test_homepage_lists_all_dealers_for_anonymous_visitors(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Classic Motors")
        self.assertContains(response, "Lone Star Auto")
        self.assertContains(response, "Jayhawk Motors")
        self.assertContains(response, "Wichita, Kansas")

    def test_homepage_filters_dealers_by_state(self):
        response = self.client.get("/", {"state": "Kansas"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jayhawk Motors")
        self.assertNotContains(response, "Classic Motors")
        self.assertNotContains(response, "Lone Star Auto")

    def test_homepage_ignores_unknown_state_filter(self):
        response = self.client.get("/", {"state": "Unknown"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Classic Motors")
        self.assertContains(response, "Jayhawk Motors")

    def test_login_page_authenticates_and_displays_logged_in_user(self):
        user = get_user_model().objects.create_user(
            username="dealer-customer", password="valid-test-password"
        )
        response = self.client.post(
            "/login/",
            {"username": user.username, "password": "valid-test-password"},
        )

        self.assertRedirects(response, "/")
        home_response = self.client.get("/")
        self.assertContains(home_response, "Logged in as")
        self.assertContains(home_response, user.username)
        self.assertContains(home_response, "Review Dealer")

    def test_anonymous_visitors_do_not_see_review_dealer_action(self):
        response = self.client.get("/")

        self.assertNotContains(response, "Review Dealer")

    def test_dealer_detail_displays_dealer_and_reviews(self):
        response = self.client.get("/dealer/1/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Classic Motors")
        self.assertContains(response, "Great customer service")

    def test_logout_clears_session(self):
        user = get_user_model().objects.create_user(
            username="logout-customer", password="valid-test-password"
        )
        self.client.force_login(user)

        response = self.client.post("/logout/")

        self.assertRedirects(response, "/")
        self.assertNotIn("_auth_user_id", self.client.session)
