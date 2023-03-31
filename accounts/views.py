from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse


@login_required
def base_view(request):
    """
    dummy view serving as home page for the time being
    TODO: remove this view
    """
    return render(request, "base.html")
