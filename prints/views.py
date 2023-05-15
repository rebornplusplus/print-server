from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

from accounts.models import SiteUser
from printserver.helpers import generate_weasyprint_doc
from .forms import PrintSubmitForm
from .models import Print


@login_required
def submit_view(request):
    if request.method == "POST":
        form = PrintSubmitForm(request.POST)
        if form.is_valid():
            user = SiteUser.objects.get(id=request.user.id)
            submission = form.save(commit=False)
            submission.user = user
            pdf_pages, pdf_path = generate_weasyprint_doc(
                content=submission.content,
                template_path="prints/print-details.html",
                css_path="css/magic.css",
                top_left_header=request.user.first_name
            )
            if user.can_print(pdf_pages):
                submission.pages = pdf_pages
                if settings.KEEP_PDF:
                    submission.pdf_path = pdf_path
                with transaction.atomic():
                    user.update_pages(submission.pages)
                    submission.save()
                    user.save()
                messages.success(
                    request,
                    "Submitted successfully. Took " + str(submission.pages) + " pages."
                )
                return redirect(reverse("home"))
            else:
                messages.error(
                    request,
                    "Cannot print the submitted document. You don't have enough pages remaining."
                )
    else:
        form = PrintSubmitForm()

    context = {
        "form": form,
    }
    return render(request, "prints/submit.html", context)


@login_required
def submissions_view(request):
    return render(request, "base.html")
