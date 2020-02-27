import django_filters
from django import forms

from .models import CustomersInfoAnalysis, Segments, PurchaseStatus


class CustomersInfoAnalysisFilter(django_filters.FilterSet):
    customer_email = django_filters.CharFilter(lookup_expr='icontains')
    segment = django_filters.ModelMultipleChoiceFilter(queryset=Segments.objects.all(),
                                                       widget=forms.CheckboxSelectMultiple)
    purchase_status = django_filters.ModelMultipleChoiceFilter(queryset=PurchaseStatus.objects.all(),
                                                               widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = CustomersInfoAnalysis
        fields = ["customer_email", "segment", "purchase_status"]
