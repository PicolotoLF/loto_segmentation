from .forms import SpreadSheetInfoForm

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required


@permission_required("google_spreadsheets.view_spreadsheetinfo", raise_exception=True)
def insert_credentials(request):
    if request.method == "POST":
        form = SpreadSheetInfoForm(request.POST, request.FILES)
        if form.is_valid():
            credentials = form.save()
            credentials.user = request.user
            credentials.save()
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect('/dashboard')
    else:
        form = SpreadSheetInfoForm()
    #     Show the credentials

    return render(request, 'google_spreadsheets/insert_credentials.html', {'form': form})

# method to edit credentials

# method to delete credential
