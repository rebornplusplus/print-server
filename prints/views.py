from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse

from .forms import PrintSubmitForm


@login_required
def submit_view(request):
    if request.method == "POST":
        form = PrintSubmitForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.pages = 1    # TODO: PLACEHOLDER. Update accordingly.
            submission.save()
            messages.success(
                request,
                "Submitted successfully. <a href=" + reverse("prints.submissions") + ">See all submissions</a>."
            )
            return redirect(reverse("home"))
    else:
        form = PrintSubmitForm()

    context = {
        "form": form,
    }
    return render(request, "prints/submit.html", context)


@login_required
def submissions_view(request):
    return render(request, "base.html")
