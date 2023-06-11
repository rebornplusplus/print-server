from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class SiteUser(AbstractUser):
    remaining_pages = models.IntegerField(default=settings.MAX_PAGES)
    organization = models.CharField(blank=True, null=True, max_length=200)
    printer = models.CharField(blank=True, null=True, max_length=200)

    def can_print(self, page_count):
        return page_count <= settings.MAX_PAGES_PER_PRINT \
            and self.remaining_pages >= page_count

    def update_pages(self, pages_printed):
        self.remaining_pages -= pages_printed
        if self.remaining_pages < 0:
            self.remaining_pages = 0

    def get_remaining_pages(self):
        return self.remaining_pages

    def get_org_name(self):
        return self.organization if self.organization else ""

    def get_printer(self):
        return self.printer if self.printer else ""
