from django.db import models
from django.contrib.auth.models import User


# https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html

class SpreadSheetInfo(models.Model):
    spreadsheet_url = models.CharField(max_length=255, unique=True)
    sheet_name = models.CharField(max_length=255)
    client_secret_file = models.FileField(upload_to="etc")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
