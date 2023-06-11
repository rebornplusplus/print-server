import csv

from django import forms
from django.contrib.auth.password_validation import MinimumLengthValidator, NumericPasswordValidator
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.exceptions import ValidationError


class AddMultipleUsersForm(forms.Form):

    class DummyUser:
        def __init__(self, record):
            if len(record) != 5:
                raise ValidationError("Invalid record: " + ",".join(record))
            self.username = record[0]
            self.password = record[1]
            self.first_name = record[2]
            self.organization = record[3]
            self.printer = record[4]
            self.validate()

        def validate(self):
            self.validate_username()
            self.validate_password()
            self.validate_first_name()

        def validate_username(self):
            ASCIIUsernameValidator().__call__(self.username)

        def validate_password(self):
            MinimumLengthValidator().validate(self.password)
            NumericPasswordValidator().validate(self.password)

        def validate_first_name(self):
            if self.first_name is None or self.first_name == "":
                raise ValidationError("Name cannot be empty")

    users_details = forms.CharField(
        label="Users list (CSV)",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "autofocus": True,
                "style": "display: block;"
                         "width: 70%;"
                         "max-width: 100%"
                         "-webkit-box-sizing: border-box;"
                         "-moz-box-sizing: border-box;"
                         "box-sizing: border-box;",
                "placeholder": "<username>,<password>,<name>,<organization>,<printer-name>\n"
                               "...",
            }
        ),
        help_text="<br/>".join([
            str(ASCIIUsernameValidator().message),
            MinimumLengthValidator().get_help_text(),
            NumericPasswordValidator().get_help_text(),
            "organization is optional and may be left empty.",
            "printer-name is optional and may be left empty. The default printer will be used if empty."
        ]),
    )

    def clean_users_details(self):
        data = self.cleaned_data["users_details"]
        # check if the attributes are valid
        # schema: username, password, first_name, organization, printer name
        user_info_list = list(csv.reader(data.split('\n'), delimiter=","))
        for user_info in user_info_list:
            self.DummyUser(user_info)
        return data
