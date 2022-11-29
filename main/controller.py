# define paths for different web pages
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("upload/", views.file_upload_optimize, name="file_upload"),
    path("filling_form/", views.click_optimize, name="form_operation"),
]
