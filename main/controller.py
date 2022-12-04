# define paths for different web pages
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),          # Run server sẽ chạy vào path mặc định, và sẽ được xử lý bởi METHOD home trong views
    path("upload/", views.file_upload_optimize, name="file_upload"),        # Ấn Optimize ở import file sẽ gọi đến path /upload, được xử lý bởi METHOD file_upload_optimize ở views
    path("filling_form/", views.click_optimize, name="form_operation"),     # Điền form rồi ấn Optimize sẽ gọi đến path /filling_form, được xử lý bởi METHOD click_optimize ở views
]
