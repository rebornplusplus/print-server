from django.conf import settings
from django.db import transaction
from django.test import TestCase
from django.urls import reverse

from accounts.models import SiteUser


def create_user(username, password, is_superuser=False):
    user = SiteUser.objects.create(username=username)
    user.set_password(password)
    user.is_staff = is_superuser
    user.is_superuser = is_superuser
    user.save()


class AccountTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "foo"
        cls.password = "bar"
        create_user(cls.username, cls.password)
        cls.admin_username = "admin"
        cls.admin_password = "admin"
        create_user(cls.admin_username, cls.admin_password, is_superuser=True)

    def test_login(self):
        # unsuccessful
        resp = self.client.post(
            settings.LOGIN_URL,
            {"username": "foo", "password": "foo"},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Please enter a correct username and password.")
        self.assertTemplateUsed(resp, "login.html")
        # successful
        resp = self.client.post(
            settings.LOGIN_URL,
            {"username": self.username, "password": self.password},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, "/")

    def test_homepage(self):
        # before login
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, settings.LOGIN_URL + "?next=/")
        # login
        self.client.login(username=self.username, password=self.password)
        # after login
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "base.html")

    def test_logout(self):
        # before login
        resp = self.client.get("/accounts/logout", follow=True)
        self.assertEqual(resp.status_code, 200)
        expected_chain = [
            ("/accounts/logout/", 301),
            ("/", 302),
            (settings.LOGIN_URL + "?next=/", 302)
        ]
        self.assertEqual(resp.redirect_chain, expected_chain)
        self.assertTemplateUsed("login.html")
        # login
        self.client.login(username=self.username, password=self.password)
        # after login
        resp = self.client.get("/accounts/logout", follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.redirect_chain, expected_chain)
        self.assertTemplateUsed("login.html")
        # home page should not be accessible now
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, settings.LOGIN_URL + "?next=/")

    def test_admin_login(self):
        # unsuccessful
        self.client.login(username=self.username, password=self.password)
        resp = self.client.get("/admin/")
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, "/admin/login/?next=/admin/")
        # successful
        self.client.login(username=self.admin_username, password=self.admin_password)
        resp = self.client.get("/admin/", follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateNotUsed(resp, "admin/login.html")

    def test_admin_bulk_user_addition(self):
        # login
        self.client.login(username=self.admin_username, password=self.admin_password)
        # access the "Users" dashboard
        resp = self.client.get(reverse("admin:accounts_siteuser_changelist"), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "admin/accounts/change_list_object_tools.html")
        # access the "Add Users in Bulk" page
        resp = self.client.get(reverse("admin:accounts_siteuser_add_users"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "admin/accounts/add_users.html")
        # create user - unsuccessful
        resp = self.client.post(
            reverse("admin:accounts_siteuser_add_users"),
            {"users_details": "bar,bar,bar"}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Failed to add the users.")
        # create user - successful
        # https://stackoverflow.com/a/23326971/5887509
        with transaction.atomic():
            resp = self.client.post(
                reverse("admin:accounts_siteuser_add_users"),
                {"users_details": "bar,password,bar"}
            )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse("admin:accounts_siteuser_changelist"))
        # check if user is created
        with transaction.atomic():
            user = SiteUser.objects.get(username="bar")
        self.assertNotEqual(user, None)
        self.assertEqual(user.get_full_name(), "bar")
        # login using the newly created user
        self.assertTrue(self.client.login(username="bar", password="password"))

