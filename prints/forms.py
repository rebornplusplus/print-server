from django import forms

from .models import Print


class PrintSubmitForm(forms.ModelForm):
    file = forms.FileField(
        required=False,
        label="Paste from file",
        widget=forms.FileInput(attrs={"onchange": "pasteContent()"}),
        help_text="Choose a text file to paste its content in the text input above."
    )

    class Meta:
        model = Print
        exclude = ("id", "created_at", "user", "pages")
        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control source-code",
                "rows": "20",
            }),
        }
