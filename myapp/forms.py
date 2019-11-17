from django import forms
from django.contrib.auth.models import User
from .models import CustomersInfoCsv
import csv


class CustomerInfoForm(forms.ModelForm):
    class Meta:
        model = CustomersInfoCsv
        fields = ["order_date", "order_value", "customer_id", "user"]


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
