import csv

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import render, redirect, reverse
from django.urls.conf import path

from .forms import AddMultipleUsersForm
from .models import SiteUser


@admin.register(SiteUser)
class SiteUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            "Print Settings",
            {
                "fields": (
                    "remaining_pages",
                )
            }
        )
    )
    add_users_form = AddMultipleUsersForm

    def get_urls(self):
        urls = [
                   path(
                       "add-users/",
                       self.admin_site.admin_view(self.add_users_view),
                       name="accounts_siteuser_add_users",
                   )
               ] + super().get_urls()
        return urls

    def add_users_view(self, request, form_url=""):
        if request.method == "POST":
            form = self.add_users_form(request.POST)
            if form.is_valid():
                added_users = []
                failed_users = []
                user_info_data = form.cleaned_data["users_details"]
                user_info_list = list(csv.reader(user_info_data.split('\n'), delimiter=","))
                for user_info in user_info_list:
                    try:
                        SiteUser.objects.create_user(
                            username=user_info[0],
                            password=user_info[1],
                            first_name=user_info[2]
                        )
                    except Exception:
                        failed_users.append(user_info[0])
                        continue
                    added_users.append(user_info[0])

                if len(added_users) > 0:
                    messages.success(
                        request,
                        "Successfully added " + str(len(added_users)) + " user(s): " + ", ".join(added_users) + "."
                    )
                if len(failed_users) > 0:
                    messages.error(
                        request,
                        "Failed to add " + str(len(failed_users)) + " user(s): " + ", ".join(failed_users) + "."
                    )

                return redirect(reverse("admin:accounts_siteuser_changelist"))
            else:
                messages.error(request, "Failed to add the users.")
        else:
            form = self.add_users_form()

        context = {
            "title": "Add Users",
            "form_url": form_url,
            "form": form,
            **self.admin_site.each_context(request),
        }

        return render(request, "admin/accounts/add_users.html", context=context)
