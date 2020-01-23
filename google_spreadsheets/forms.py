from django import forms
from .models import SpreadSheetInfo


class SpreadSheetInfoForm(forms.ModelForm):
    class Meta:
        model = SpreadSheetInfo
        exclude = ["user"]
