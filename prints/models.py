from django.db import models

from accounts.models import SiteUser


class Print(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name="user")
    source_code = models.TextField()
    pages = models.IntegerField()
