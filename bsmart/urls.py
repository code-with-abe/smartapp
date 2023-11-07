from django.urls import path
from bsmart import views

urlpatterns = [
    path('', views.index, name='index'),
    
]