from django.shortcuts import render
from .forms import FileUploadForm
from .handle_cutting_stock import *
from django.http import JsonResponse


# Create your views here, all view of my application will be here
def home(request):
    form = FileUploadForm()
    return render(request, "main/home.html", {'form': form})


def file_upload_optimize(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        handle_uploaded_file(request.FILES['file'])
        print("here")
        status, cutting_instruction_list, optimal_value = get_cutting_instruction_by_uploading_file()
        return JsonResponse(
            {'status': status, 'optimal_value': optimal_value, 'cutting_instruction_list': cutting_instruction_list})


def click_optimize(request):
    properties = dict(request.POST)
    print(properties)
    status, cutting_instruction_list, optimal_value = get_cutting_instruction_by_filling(properties)
    return JsonResponse(
        {'status': status, 'optimal_value': optimal_value, 'cutting_instruction_list': cutting_instruction_list})
