# Generated by Django 2.2.6 on 2019-11-06 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('google_spreadsheets', '0002_auto_20191105_0228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spreadsheetinfo',
            name='client_secret_file',
            field=models.FileField(upload_to='etc'),
        ),
    ]
