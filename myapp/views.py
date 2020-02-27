# Create your views here.
import csv
import io
import json

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.aggregates import Count
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django_tables2 import SingleTableView
from django_tables2.export.export import TableExport
from django_tables2.config import RequestConfig
from django_filters.views import FilterView

from .filters import CustomersInfoAnalysisFilter
from .forms import UploadFileForm, UserForm, ConfigRFMForm
from .models import CustomersInfoCsv, CustomersInfoAnalysis, CustomerInfoBoundary, ConfigRFM
from .services import RFMCalculator
from .tables import CustomersInfoAnalysisTable


def index(request):
    return HttpResponseRedirect('accounts/login')


def generic(request):
    return render(request, "base_generic.html")


def create_account(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect('upload_customer_info_csv')
    else:
        form = UserForm()

    return render(request, 'registration/create_account.html', {'form': form})


@login_required
def welcome_page(request):
    if request.session['username'] == "teste":
        pass
    # Page with instructions to new users
    # Its necessary to validate all this fields
    # 1 - Prepare and upload a CSV
    # 2 - Set up de Boundaries
    # 3 - Calculate
    pass


@login_required
def dashboard(request):
    qtd_segments = CustomersInfoAnalysis.objects.filter(user=request.user) \
        .all().values("segment__title").annotate(qtd=Count('segment'))

    qtd_purcharse_status = CustomersInfoAnalysis.objects.filter(user=request.user) \
        .all().values("purchase_status__title").annotate(qtd=Count('purchase_status'))

    qtd_customers = CustomersInfoAnalysis.objects.filter(user=request.user).count()

    values = CustomerInfoBoundary.objects.filter(user=request.user).first()
    if values is None:
        boundary_frequency = 0
        boundary_monetary = 0
        ensure_calculate = True
    else:
        boundary_monetary = values.boundary_monetary
        boundary_frequency = int(values.boundary_frequency)
        ensure_calculate = False

    return render(request, "example_dashboard.html", {
        "qtd_purchase_status": json.dumps(list(qtd_purcharse_status)),
        "qtd_segments": json.dumps(list(qtd_segments)),
        "boundary_frequency": boundary_frequency,
        "boundary_monetary": boundary_monetary,
        "qtd_customers": qtd_customers,
        "ensure_calculate": ensure_calculate
    })


@login_required
def upload_file(request):
    form = UploadFileForm()
    if request.method == 'POST':
        upload_file_form = UploadFileForm(request.POST, request.FILES)
        print("csv" in str(upload_file_form.files["file"]))
        if upload_file_form.is_valid():
            csv_file_buffer = io.TextIOWrapper(request.FILES["file"])
            csv_file = csv.DictReader(csv_file_buffer, delimiter=",")
            if "csv" not in str(upload_file_form.files["file"]):
                return render(request, 'upload_customer_info_csv.html', {'form': form, "wrong_csv": True})

            if "order_date" not in csv_file.fieldnames or "order_value" not in csv_file.fieldnames \
                    or "customer_email" not in csv_file.fieldnames:
                return render(request, 'upload_customer_info_csv.html', {'form': form, "wrong_csv": True})

            CustomersInfoCsv.objects.filter(user=request.user).delete()
            for info in csv_file:
                print(info["customer_email"])
                new_customer_info = CustomersInfoCsv.objects.create(order_date=info["order_date"],
                                                                    order_value=info["order_value"],
                                                                    customer_email=info["customer_email"],
                                                                    user=request.user)
                new_customer_info.save()

            return HttpResponseRedirect("config_rfm")

    return render(request, 'upload_customer_info_csv.html', {'form': form, "wrong_csv": False})


@login_required
def config_rfm(request):
    if request.method == "POST":
        form = ConfigRFMForm(request.POST)
        if form.is_valid():
            # ** form.cleaned_data,
            new_config_rfm, created = ConfigRFM.objects.update_or_create(user=request.user,
                                                                         defaults={**form.cleaned_data})
            # if created is False:
            #     new_config_rfm = ConfigRFM.objects.create(**form.cleaned_data, user=request.user)

            new_config_rfm.save()
            return HttpResponseRedirect('config_rfm')
    else:
        try:
            config_rfm_obj = ConfigRFM.objects.get(user=request.user)
            form = ConfigRFMForm(instance=config_rfm_obj)
        except Exception as e:
            print(e)
            form = ConfigRFMForm()

    return render(request, 'config_rfm.html', {'form': form})


@login_required
def table_customer_info_analysis(request):
    values = CustomersInfoAnalysis.objects.select_related("segment").filter(user=request.user).all()
    values_filter = CustomersInfoAnalysisFilter(request.GET, queryset=values)
    table = CustomersInfoAnalysisTable(values_filter.qs)
    table.paginate(page=request.GET.get("page", 1), per_page=25)

    RequestConfig(request).configure(table)
    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response("lot_segmentation.{}".format(export_format))

    return render(request, "table_customer_info_analysis.html", {
        "table": table,
        "values_filter": values_filter
    })


@login_required
def task_calculate_customers_info(request):
    # This will be a task, but for now I am using to test
    CustomersInfoAnalysis.objects.filter(user=request.user).delete()
    CustomerInfoBoundary.objects.filter(user=request.user).delete()
    # ConfigRFM.objects.filter(user=request.user).delete()

    values = CustomersInfoCsv.objects.filter(user=request.user).values("order_date", "order_value", "customer_email")
    config_rfm_values = ConfigRFM.objects.filter(user=request.user).first()
    calculator = RFMCalculator(list(values), config_rfm_values.score_boundary_frequency,
                               config_rfm_values.score_boundary_monetary,
                               config_rfm_values.limit_days)
    calculator.calculate_values()
    values = calculator.to_dict()

    model_instances = [CustomersInfoAnalysis(

        order_date=record["order_date"],
        monetary=record["monetary"],
        customer_email=record["customer_email"],
        frequency=record["frequency"],
        avg_monetary=record["avg_monetary"],
        recency=record["recency"],
        first_purchase=record["first_purchase"],
        avg_days=record["diff_date"],
        std_dev_days=record["std_dev"],
        score_frequency=record["score_frequency"],
        score_monetary=record["score_monetary"],
        segment=record["segment"],
        purchase_status=record["purchase_status"],
        user=request.user
    ) for record in values]

    CustomersInfoAnalysis.objects.bulk_create(model_instances)

    CustomerInfoBoundary.objects.create(boundary_frequency=calculator.boundary_frequency,
                                        boundary_monetary=calculator.boundary_monetary,
                                        user=request.user).save()

    return render(request, "example_dashboard.html")
