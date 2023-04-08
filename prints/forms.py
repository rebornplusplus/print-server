from django import forms

from .models import Print


class PrintSubmitForm(forms.ModelForm):
    file = forms.FileField(
        required=False,
        label="Paste from File",
        widget=forms.FileInput(attrs={"onchange": "pasteContent()"}),
        help_text="Choose a text file to paste its content to the Source Code field above."
    )

    class Meta:
        model = Print
        exclude = ("id", "created_at", "user", "pages")
        widgets = {
            "source_code": forms.Textarea(attrs={"class": "form-control"}),
        }
        labels = {
            "source_code": "Source Code",
        }
