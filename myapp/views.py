# Create your views here.
import csv
import io

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render


from google_spreadsheets.models import SpreadSheetInfo
from .forms import UploadFileForm, UserForm
from .models import CustomersInfoCsv, CustomersInfoAnalysis, CustomerInfoBoundary
from .services import get_values_from_spreadsheet, RFMCalculator


def index(request):
    return render(request, 'index.html')


def generic(request):
    return render(request, "base_generic.html")


def create_account(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect('dashboard')
    else:
        form = UserForm()

    return render(request, 'registration/create_account.html', {'form': form})


@login_required
def dashboard(request):
    print(dir(request.user))
    values = CustomerInfoBoundary.objects.filter(user=request.user).first()
    return render(request, "example_dashboard.html", {"boundary_frequency": values.boundary_frequency,
                                                      "boundary_monetary": values.boundary_monetary})


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file_buffer = io.TextIOWrapper(request.FILES["file"])
            csv_file = csv.DictReader(csv_file_buffer, delimiter=",")
            CustomersInfoCsv.objects.filter(user=request.user).delete()
            for info in csv_file:
                new_customer_info = CustomersInfoCsv.objects.create(order_date=info["order_date"],
                                                                    order_value=info["order_value"],
                                                                    customer_email=info["customer_email"],
                                                                    user=request.user)
                new_customer_info.save()

            return HttpResponseRedirect("dashboard")
    else:
        form = UploadFileForm()
    return render(request, 'upload_customer_info_csv.html', {'form': form})


@login_required
def customer_info_table_csv(request):
    # Show in a table all the information from customersinfo table, allowing CRUD to the user
    values = CustomersInfoCsv.objects.filter(user=request.user)

    return render(request, 'customer_info_table.html', {"values": values})


@login_required
def customers_rfm_csv(request):
    # SpreadSheet it's need's to be a factory
    values = CustomersInfoAnalysis.objects.select_related("segment").filter(user=request.user).all()

    return render(request, 'customers_info.html', {"values": values})


@login_required
def task_calculate_customers_info(request):
    # This will be a task, but for now I am using to test
    CustomersInfoAnalysis.objects.filter(user=request.user).delete()
    CustomerInfoBoundary.objects.filter(user=request.user).delete()

    values = CustomersInfoCsv.objects.filter(user=request.user).values("order_date", "order_value", "customer_email")

    calculator = RFMCalculator(list(values), 3, 4, 13)
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
        user=request.user
    ) for record in values]

    CustomersInfoAnalysis.objects.bulk_create(model_instances)

    CustomerInfoBoundary.objects.create(boundary_frequency=calculator.boundary_frequency,
                                        boundary_monetary=calculator.boundary_monetary,
                                        user=request.user).save()

    return render(request, "example_dashboard.html")
