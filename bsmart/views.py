from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from django.conf import settings

from .process_file import process_csv

# Create your views here.
def index(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard or any other page after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    return auth_views.LoginView.as_view(template_name='login.html')(request)

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def upload(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        # Handle the uploaded file here (save it, process it, etc.)
        # For example, you can save the file to the media folder:
        with open('media/' + uploaded_file.name, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
                
        if upload_to_adls(uploaded_file.name):
            return render(request, 'dashboard.html')
        else:
            # Return an error response
            return HttpResponse('Failed to upload file', status=500)
    return render(request, 'upload.html')

# Initialize Azure Blob Service Client with your connection string

container_url = settings.AZURE_CONTAINER_SAS

def upload_to_adls(uploaded_file_name):
    try:

        container_client = ContainerClient.from_container_url(container_url)
        
        blob_name = "diabetes/bsmart_uploads/"+uploaded_file_name
        # Upload the file to Azure storage
        # Get a BlobClient to represent the blob we are creating
        blob_client = container_client.get_blob_client(blob=blob_name)
        with open('media/' + uploaded_file_name, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        # Return True if the file has been uploaded successfully
        return True
    except Exception as e:
        # Handle exceptions
        print(e)
        return False