# Generated by Django 3.0.2 on 2020-02-28 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20200216_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customersinfocsv',
            name='order_value',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
