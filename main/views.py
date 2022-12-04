from django.shortcuts import render
from .forms import FileUploadForm
from .handle_cutting_stock import *
import os


# Create your views here, all view of my application will be here
# Method xử lý cho path mặc định
def home(request):
    form = FileUploadForm()         # Tạo trước một form ở class FileUploadForm, dùng sẵn chức năng tạo field cho form của framework để giảm thiểu code
    return render(request, "main/home.html", {'form': form})                      # Trả dữ liệu form cho form ở homepage (Nút Browse là trường File đó)


# Method xử lý nếu upload file
def file_upload_optimize(request):
    if request.method == "POST":
        # Xử lý file đc upload.
        handle_uploaded_file(request.FILES['file'])
        # Sau khi lưu đc vào file input, thực hiện Method get_cutting_instruction_by_uploading_file() để lấy ra kết quả.
        fixed_length, (cutting_instruction_list,
                       optimal_value) = get_cutting_instruction_by_uploading_file()

        list_color = ['red', 'blue', 'green', 'yellow', 'pink',
                      'purple', 'orange', 'brown', 'black']

        # Define context for rendering
        response_context = {'fixed_length': int(fixed_length), 'optimal_value': int(optimal_value),
                            'cutting_instruction_list':  [{'number': int(cutting_instruction['number']), 'type': [{'value': int(x), 'color': list_color[cutting_instruction['type'].index(x) % len(list_color)]} for x in cutting_instruction['type']], 'residual': int(cutting_instruction['residual'])} for cutting_instruction in cutting_instruction_list],
                            }
        # Path to CWD - nối đường dẫn để đến trang hiển thị kết quả - template_name, dữ liệu đc truyền - context
        cwd = os.getcwd()
        path_template_result = os.path.join(
            cwd, 'main', 'templates', 'main', 'result.html')
        # Render the result page
        return render(request=request, template_name=path_template_result, context=response_context)


# Method xử lý nếu click form, cũng gần giống nếu thực hiện với upload file.
def click_optimize(request):
    properties = dict(request.POST)     # Lấy ra thông tin được điền bởi client
    print(properties)
    # Truyền thông tin lấy đc vào hàm get_cutting_instruction_by_filling(properties) để xử lý và lấy ra kết quả.
    fixed_length, (cutting_instruction_list,
                   optimal_value) = get_cutting_instruction_by_filling(properties)

    # Khai báo các màu ...
    list_color = ['red', 'blue', 'green', 'yellow', 'pink',
                  'purple', 'orange', 'brown', 'black']

    # Define context for rendering
    response_context = {'fixed_length': int(fixed_length), 'optimal_value': int(optimal_value),
                        'cutting_instruction_list':  [{'number': int(cutting_instruction['number']), 'type': [{'value': int(x), 'color': list_color[cutting_instruction['type'].index(x) % len(list_color)]} for x in cutting_instruction['type']], 'residual': int(cutting_instruction['residual'])} for cutting_instruction in cutting_instruction_list],
                        }

    # Path to CWD - nối đường dẫn để đến trang hiển thị kết quả - template_name, dữ liệu đc truyền - context
    cwd = os.getcwd()
    path_template_result = os.path.join(
        cwd, 'main', 'templates', 'main', 'result.html')
    # Render the result page
    return render(request=request, template_name=path_template_result, context=response_context)
