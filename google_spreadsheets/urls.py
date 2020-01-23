from django.urls import path

from . import views

urlpatterns = [
  path('insert_credentials', views.insert_credentials, name='insert_credentials'),
]