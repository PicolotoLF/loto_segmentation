# Generated by Django 3.0.2 on 2020-02-13 00:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfigRFM',
            fields=[
                ('limit_days', models.IntegerField()),
                ('score_boundary_frequency', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('score_boundary_monetary', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseStatus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Segments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CustomersInfoCsv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateField()),
                ('order_value', models.IntegerField()),
                ('customer_email', models.EmailField(max_length=255)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomersInfoAnalysis',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('order_date', models.DateField()),
                ('monetary', models.IntegerField()),
                ('customer_email', models.CharField(max_length=255)),
                ('frequency', models.IntegerField()),
                ('avg_monetary', models.FloatField()),
                ('recency', models.IntegerField()),
                ('first_purchase', models.IntegerField()),
                ('avg_days', models.FloatField()),
                ('std_dev_days', models.FloatField()),
                ('score_frequency', models.IntegerField()),
                ('score_monetary', models.IntegerField()),
                ('purchase_status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.PurchaseStatus')),
                ('segment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.Segments')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerInfoBoundary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('boundary_frequency', models.FloatField()),
                ('boundary_monetary', models.FloatField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
