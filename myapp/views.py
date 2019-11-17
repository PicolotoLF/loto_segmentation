# Create your views here.
import csv
import io

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response

from google_spreadsheets.models import SpreadSheetInfo
from .forms import UploadFileForm, UserForm
from .models import CustomersInfoCsv, CustomersInfoAnalysis, CustomerInfoBoundary
from .services import get_values_from_spreadsheet, RFMCalculator


def index(request):
    return render_to_response('index.html')


def generic(request):
    return render_to_response("base_generic.html")


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
    values = CustomerInfoBoundary.objects.filter(user=request.user).first()
    return render(request, "example_dashboard.html", {"boundary_frequency": values.boundary_frequency,
                                                      "boundary_monetary": values.boundary_monetary})


@login_required
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file_buffer = io.TextIOWrapper(request.FILES["file"])
            csv_file = csv.DictReader(csv_file_buffer, delimiter=";")
            for info in csv_file:
                new_customer_info = CustomersInfoCsv.objects.create(order_date=info["order_date"],
                                                                    order_value=info["order_value"],
                                                                    customer_id=info["customer_id"],
                                                                    user=request.user)
                new_customer_info.save()

            return HttpResponseRedirect("dashboard")
    else:
        form = UploadFileForm()
    return render(request, 'upload_customer_info_csv.html', {'form': form})


def customer_info_table_csv(request):
    # Show in a table all the information from customersinfo table, allowing CRUD to the user
    values = CustomersInfoCsv.objects.filter(user=request.user)

    return render(request, 'customer_info_table.html', {"values": values})


def customers_info_table_google_sheets_detailed(request):
    # SpreadSheet it's need's to be a factory
    values = CustomersInfoAnalysis.objects.filter(user=request.user).all()

    return render(request, 'customers_info.html', {"values": values})


def task_calculate_customers_info(request):
    # This will be a task, but for now I am using to test
    CustomersInfoAnalysis.objects.filter(user=request.user).delete()
    CustomerInfoBoundary.objects.filter(user=request.user).delete()

    spread_sheet_info = SpreadSheetInfo.objects.filter(user=request.user).first()

    values = get_values_from_spreadsheet(spread_sheet_info.client_secret_file,
                                         spread_sheet_info.spreadsheet_url,
                                         spread_sheet_info.sheet_name)

    calculator = RFMCalculator(values, 3, 4)
    calculator.calculate_values()
    values = calculator.to_dict()

    model_instances = [CustomersInfoAnalysis(

        order_date=record["order_date"],
        monetary=record["monetary"],
        customer_id=record["customer_id"],
        frequency=record["frequency"],
        avg_monetary=record["avg_monetary"],
        recency=record["recency"],
        first_purchase=record["first_purchase"],
        avg_days=record["diff_date"],
        std_dev_days=record["std_dev"],
        score_frequency=record["score_frequency"],
        score_monetary=record["score_monetary"],
        user=request.user
    ) for record in values]

    CustomersInfoAnalysis.objects.bulk_create(model_instances)

    CustomerInfoBoundary.objects.create(boundary_frequency=calculator.boundary_frequency,
                                        boundary_monetary=calculator.boundary_monetary,
                                        user=request.user).save()

    return render(request, "example_dashboard.html")


def results(request):
    # Show the segments
    return
