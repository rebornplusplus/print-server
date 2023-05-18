from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db import transaction
from django.shortcuts import render, redirect, reverse

from accounts.models import SiteUser
from .helpers import generate_pdf
from .forms import PrintSubmitForm
from .printer import check_printer_daemon, submit_to_printer


if not check_printer_daemon():
    print("error: printer daemon (e.g. `lpr') not found.")


@login_required
def submit_view(request):
    if request.method == "POST":
        form = PrintSubmitForm(request.POST)
        if form.is_valid():
            user = SiteUser.objects.get(id=request.user.id)
            submission = form.save(commit=False)
            submission.user = user
            pdf_pages, pdf_path = generate_pdf(submission.content, user)
            if user.can_print(pdf_pages):
                submission.pages = pdf_pages
                submission.pdf_path = pdf_path
                with transaction.atomic():
                    user.update_pages(submission.pages)
                    submission.save()
                    user.save()
                if check_printer_daemon():
                    submit_to_printer(settings.MEDIA_ROOT + "/" + pdf_path)
                    messages.success(
                        request,
                        "Submission sent to printer. Took " + str(submission.pages) + " pages."
                    )
                else:
                    messages.info(
                        request,
                        "Submission saved. printer-daemon not available. Took " + str(submission.pages) + " pages."
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
