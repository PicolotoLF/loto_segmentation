from django import forms
from django.contrib.auth.models import User
from .models import CustomersInfoCsv, ConfigRFM


class CustomerInfoForm(forms.ModelForm):
    class Meta:
        model = CustomersInfoCsv
        fields = ["order_date", "order_value", "customer_email"
                                               "", "user"]


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')


class ConfigRFMForm(forms.ModelForm):
    class Meta:
        model = ConfigRFM
        fields = ("limit_days", "score_boundary_frequency", "score_boundary_monetary")
