from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from django.conf import settings
from .models import FileStatus 
from django.utils import timezone
import uuid
import os
import logging

from .process_file import process_csv

logger = logging.getLogger(__name__)

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
    """
    Handles file uploads and displays recent uploads.
    """
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        
        # Generate a new filename with a standard prefix and random UUID
        _, file_extension = os.path.splitext(uploaded_file.name)
        new_file_name = f"med780g_{uuid.uuid4()}{file_extension}"

        try:
            file_path = save_file_locally(uploaded_file)
            if upload_to_adls(file_path):
                FileStatus.objects.create(file_name=uploaded_file.name, status="Uploaded Successfully")
            else:
                FileStatus.objects.create(file_name=uploaded_file.name, status="Failed to Upload", upload_timestamp=timezone.now())
        except Exception as error:
            logger.error("Upload error: %s", error)
            return HttpResponse(f'Error during file upload: {error}', status=500)

    recent_uploads = FileStatus.objects.order_by('-upload_timestamp')[:3]
    return render(request, 'upload.html', {'recent_uploads': recent_uploads})


def save_file_locally(uploaded_file):
    """
    Saves an uploaded file locally in the media directory.
    """
    file_path = settings.MEDIA_ROOT + '/' + uploaded_file.name
    if not default_storage.exists(file_path):
        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
    return file_path




def upload_to_adls(file_path, container_url=settings.AZURE_CONTAINER_SAS, blob_path_prefix="diabetes/bsmart_uploads/"):
    """
    Uploads a file to Azure Data Lake Storage (ADLS).

    Args:
    - file_path: Full path of the file to upload.
    - container_url: URL of the Azure container. Defaults to the one defined in settings.
    - blob_path_prefix: Prefix path for the blob in ADLS.

    Returns:
    - True if upload succeeds, False otherwise.
    """
    try:
        container_client = ContainerClient.from_container_url(container_url)
        file_name = file_path.split('/')[-1]
        blob_name = f"{blob_path_prefix}{file_name}"

        blob_client = container_client.get_blob_client(blob=blob_name)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        return True
    except Exception as e:
        logger.error("Failed to upload to ADLS: %s", e)
        return False