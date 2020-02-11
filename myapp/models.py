from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CustomersInfoCsv(models.Model):
    order_date = models.DateField(null=False)
    order_value = models.IntegerField(null=False)
    customer_email = models.EmailField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class Segments(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)

    def __repr__(self):
        return self.title


class CustomersInfoAnalysis(models.Model):
    order_date = models.DateField(null=False)
    monetary = models.IntegerField(null=False)
    customer_email = models.CharField(max_length=255, null=False)
    frequency = models.IntegerField(null=False)
    avg_monetary = models.FloatField(null=False)
    recency = models.IntegerField(null=False)
    first_purchase = models.IntegerField(null=False)
    avg_days = models.FloatField(null=False)
    std_dev_days = models.FloatField(null=False)
    score_frequency = models.IntegerField(null=False)
    score_monetary = models.IntegerField(null=False)

    segment = models.ForeignKey(Segments, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class CustomerInfoBoundary(models.Model):
    boundary_frequency = models.FloatField(null=False)
    boundary_monetary = models.FloatField(null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

