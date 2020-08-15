from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.


class CustomersInfoCsv(models.Model):
    order_date = models.DateField(null=False)
    order_value = models.DecimalField(max_digits=10, decimal_places=2)
    customer_email = models.EmailField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class Segments(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.title


class PurchaseStatus(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.title


class CustomersInfoAnalysis(models.Model):
    id = models.AutoField(primary_key=True)
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

    purchase_status = models.ForeignKey(PurchaseStatus, on_delete=models.SET_NULL, null=True)
    segment = models.ForeignKey(Segments, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CustomerInfoBoundary(models.Model):
    boundary_frequency = models.FloatField()
    boundary_monetary = models.FloatField()
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )


class ConfigRFM(models.Model):
    limit_days = models.IntegerField()
    score_boundary_frequency = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    score_boundary_monetary = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

