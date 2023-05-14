from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class SiteUser(AbstractUser):
    remaining_pages = models.IntegerField(default=settings.MAX_PAGES)

    def can_print(self, page_count):
        return self.remaining_pages >= page_count

    def update_pages(self, pages_printed):
        self.remaining_pages -= pages_printed
        if self.remaining_pages < 0:
            self.remaining_pages = 0
