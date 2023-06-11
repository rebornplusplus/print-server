from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from accounts.tests import create_user


class PrintTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = "print-user"
        cls.password = "print-password"
        user = create_user(cls.username, cls.password)
        user.organization = "print-org"
        user.save()

    def test_submit(self):
        # login
        self.client.login(username=self.username, password=self.password)
        # check that the submit page is up
        resp = self.client.get(reverse("prints.submit"))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "prints/submit.html")
        # check that submit works
        resp = self.client.post(
            reverse("prints.submit"),
            {"content": "foo"}
        )
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, reverse("home"))

    def test_large_submit(self):
        # login
        self.client.login(username=self.username, password=self.password)
        # large submits should not work
        large_content = ""
        for i in range(5000):
            large_content += "foo\n"
        resp = self.client.post(
            reverse("prints.submit"),
            {"content": large_content}
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Cannot print the submitted document.")

    def test_submit_without_login(self):
        # should not be able to access the submit page
        resp = self.client.get(reverse("prints.submit"))
        self.assertEqual(resp.status_code, 302)
        self.assertRedirects(resp, settings.LOGIN_URL + "?next=" + reverse("prints.submit"))

