from django.shortcuts import render
from .forms import FileUploadForm
from .handle_cutting_stock import *
import os


# Create your views here, all view of my application will be here
def home(request):
    form = FileUploadForm()
    return render(request, "main/home.html", {'form': form})


def file_upload_optimize(request):
    if request.method == "POST":
        FileUploadForm(request.POST, request.FILES)
        handle_uploaded_file(request.FILES['file'])
        fixed_length, (cutting_instruction_list,
                       optimal_value) = get_cutting_instruction_by_uploading_file()
        list_color = ['red', 'blue', 'green', 'yellow', 'pink',
                      'purple', 'orange', 'brown', 'black']

        # Define context for rendering
        response_context = {'fixed_length': int(fixed_length), 'optimal_value': int(optimal_value),
                            'cutting_instruction_list':  [{'number': int(cutting_instruction['number']), 'type': [{'value': int(x), 'color': list_color[cutting_instruction['type'].index(x) % len(list_color)]} for x in cutting_instruction['type']], 'residual': int(cutting_instruction['residual'])} for cutting_instruction in cutting_instruction_list],
                            }
        # Path to CWD
        cwd = os.getcwd()
        path_template_result = os.path.join(
            cwd, 'main', 'templates', 'main', 'result.html')
        # Render the result page
        return render(request=request, template_name=path_template_result, context=response_context)


def click_optimize(request):
    properties = dict(request.POST)
    print(properties)
    fixed_length, (cutting_instruction_list,
                   optimal_value) = get_cutting_instruction_by_filling(properties)
    list_color = ['red', 'blue', 'green', 'yellow', 'pink',
                  'purple', 'orange', 'brown', 'black']

    # Define context for rendering
    response_context = {'fixed_length': int(fixed_length), 'optimal_value': int(optimal_value),
                        'cutting_instruction_list':  [{'number': int(cutting_instruction['number']), 'type': [{'value': int(x), 'color': list_color[cutting_instruction['type'].index(x) % len(list_color)]} for x in cutting_instruction['type']], 'residual': int(cutting_instruction['residual'])} for cutting_instruction in cutting_instruction_list],
                        }
    # Path to CWD
    cwd = os.getcwd()
    path_template_result = os.path.join(
        cwd, 'main', 'templates', 'main', 'result.html')
    # Render the result page
    return render(request=request, template_name=path_template_result, context=response_context)
