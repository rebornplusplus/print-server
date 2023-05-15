from django.db import models

from accounts.models import SiteUser


class Print(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(SiteUser, on_delete=models.CASCADE, related_name="user")
    content = models.TextField()
    pages = models.IntegerField()
    pdf_path = models.CharField(blank=True, null=True, max_length=100)
