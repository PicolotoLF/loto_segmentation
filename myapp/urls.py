from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('upload_customer_info_csv', views.upload_file, name="upload_customer_info_csv"),
    path('create_account', views.create_account, name="create_account"),
    path('customers_rfm_csv', views.customers_rfm_csv,
         name="customers_rfm_csv"),
    path("task_calculate", views.task_calculate_customers_info, name="task_calculate"),

    path('generic', views.generic, name="generic"),
]
