from gurobipy import *

output_file = "main/static/output.txt"


# Nói chung hàm này lấy thông tin từ file truyền vào và viết lại vào file input.txt
def handle_uploaded_file(f):
    with open('main/static/upload/input.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def gurobi_solve(obj, A, x, numberOfType):  # min obj sub Ax >= b
    print("Gurobi Solve")
    model = Model()
    x_var = model.addVars(x, name="variable", vtype=GRB.INTEGER)            # Thêm biến và các điều kiện cho biến (nguyên)
    model.setObjective(quicksum(obj[i] * x_var[i] for i in x), GRB.MINIMIZE)    # Hàm mục tiêu
    for i in range(0, len(A)):
        model.addConstr(quicksum(A[i][j] * x_var[j]                         # Ràng buộc
                                 for j in x) >= numberOfType[i])
    model.optimize()                                                            # Giải
    return model


def gurobi_show(fixed_length, model, output_data, pattern):
    output_data.write("Status gurobi: " + str(model.status) + "\n")
    cutting_instruction_list = []

    for i in range(len(model.getVars())):
        root = model.getVars()[i]
        if root.x > 0:
            # Thông tin của mỗi pattern, mỗi pattern cần cắt sẽ có:
            # số lượng mỗi loại - number, cách cắt - type, phần dư - residual (có thể xem trong file output.txt)
            pattern_info = {"number": root.x, "type": pattern[i], "residual": float(fixed_length-sum(pattern[i]))}  # added residual
            # Viết ra file output trc để tiện theo dõi model khi chưa có web page
            output_data.write(
                str(root.varName) + " = " +
                str(root.x) + "\t" + str(pattern[i]) + "\n"
            )

            # Json hoàn chỉnh để truy cập vào các pattern.
            cutting_instruction_list.append(pattern_info)

    optimal_value = model.objVal
    output_data.write("Optimal value gurobi = " + str(optimal_value) + "\n")
    return cutting_instruction_list, optimal_value          # Trả về hướng dẫn cắt, giá trị tối ưu để hiển thị lên webpage


def solve(pattern: list, s: list, fixed_length: int, types: list, j: int, lowerBound: float):
    if j == len(types) - 1:
        s_c = s.copy()
        while types[j] <= fixed_length:
            s_c.append(types[j])
            fixed_length -= types[j]
        if fixed_length < lowerBound:
            pattern.append(s_c)
        return
    else:
        c: int = int(fixed_length / types[j])
        for i in range(0, c + 1):
            for k in range(0, i):
                s.append(types[j])
            solve(pattern, s, fixed_length -
                  types[j] * i, types, j + 1, lowerBound)
            for k in range(0, i):
                s.pop()


def get_frequency_of_types_in_patterns(types, pattern, lengthlist):
    var = []

    for i in range(0, len(pattern)):
        var.append("x" + str(i + 1))    # Tạo các biến để đưa vào mô hình tưh

    a = [[0 for i in range(0, len(pattern))] for j in range(0, int(lengthlist))]
    print(types)
    for i in range(0, len(pattern)):
        for j in range(0, len(pattern[i])):
            a[types.index(pattern[i][j])][i] += 1

    # Thể hiện số lần các thanh có chiều dài yêu cầu được cắt trong các patterns có thể được cắt
    # đây sẽ đc dùng làm các ràng buộc cho mô hình tư                                       (3)
    print("a[] = ", a)
    A = []      # Lưu các biến tương ứng với số lần của nó để có thể thêm vào ràng buộc cho mô hình tối ưu (3)
    for i in range(0, len(a)):
        A.append({})
        for j in range(0, len(var)):
            A[i][var[j]] = a[i][j]

    obj = {i: 1 for i in var}   # hàm mục tiêu
    return A, obj, var


def main(func):
    output_data = open(output_file, "w")
    fixed_length, types, numberOfTypes = func       # Lấy các dữ liệu cần thiết từ hàm xử lý đc truyền vào.
    lowerBound = types[len(types) - 1]
    pattern = []
    solve(pattern, [], fixed_length, types, 0, lowerBound)      # Hàm solve() lấy ra các pattern[] có thể có của các types [] đc yêu cầu. (2)
    print("Possible patterns: ", pattern)
    length_list = len(types)
    # Lấy ra các ràng buộc - A, hàm mục tiêu - obj, biến - var để thực hiện giải bttư
    A, obj, var = get_frequency_of_types_in_patterns(types, pattern, length_list)
    print("\n\n")
    model = gurobi_solve(obj=obj, A=A, x=var, numberOfType=numberOfTypes)   # Giải bài toán tối ưu, lưu kết quả vào model
    return fixed_length, gurobi_show(fixed_length, model, output_data, pattern)     # Trả về giá trị để show lên web page


# Dựa vào thuộc tính đã điền vào form để lấy ra 3 thông tin cần thiết:
# độ dài có sẵn - [] các loại (chiều dài) cần cắt - [] số lượng cho từng loại
def get_required_panels_by_filling(properties):
    required = []
    # Do thông tin lấy về có dạng json (hay dict) nên ta chỉ cần quan tâm đến value của nó (key là name)    (1)
    for k, v in properties.items():
        required.append(v[0])

    # Chiều dài thanh cần cắt ở vị trí đầu
    fixed_length = float(required[0])
    # Các request sau đó sẽ tồn tại theo dạng: length - quantity
    # Tương ứng các vị trí: 1-2, 3-4, 5-6
    listRequest = {}
    start = 1
    for i in range(1, len(required)):
        if start + 1 >= len(required):
            break

        # types (length)
        m1 = int(required[start])
        # quantity
        m2 = int(required[start + 1])
        if not m1 in listRequest:
            listRequest[m1] = m2
        else:
            listRequest[m1] += m2
        start += 2

    # Từ điển lúc này có dạng key là các type, value là quantity tương ứng với độ dài đó, sắp xếp theo key giảm dần
    listRequest = {i: listRequest[i] for i in sorted(listRequest, reverse=True)}

    # Liệt kê các types: vd. 8m, 6m, 4m, 2m
    types = [i for i in listRequest.keys()]

    # Tương ứng với types liệt kê ra số lượng: vd. 6, 8, 3, 7
    numberOfTypes = [i for i in listRequest.values()]
    fixed_length = float(fixed_length)

    # Nếu nhập một thanh cần ắt có độ dài lớn hơn thanh có sẵn thì vô lý, nên ta cho độ dài thanh sẵn có = max của thanh cần cắt
    if fixed_length < types[0]:
        fixed_length = types[0]
    return fixed_length, types, numberOfTypes


def get_cutting_instruction_by_filling(properties):
    # Lấy dữ liêu cần thiết qua hàm method get_required_panels_by_filling(properties), rồi cho vào hàm main để xử lý tiếp.
    return main(get_required_panels_by_filling(properties))


# Tương tự với upload file, ta cũng cần xử lý dữ liệu để lấy đc 3 thông tin:
# độ dài có sẵn - [] các loại (chiều dài) cần cắt - [] số lượng cho từng loại
def get_required_panels_by_uploading_file():
    # Mở file input đã lưu.
    with open("main/static/upload/input.txt") as file:
        listRequest = {}
        numb_of_requests = 0

        # Đọc theo từng dòng
        while line := file.readline().rstrip():
            request = line.split()
            if len(request) == 1:      # Dòng 1 hoặc 2, do chỉ có 1 giá trị
                if numb_of_requests == 0:
                    numb_of_requests = request[0]      # dòng 1 là số lượng request.
                else:
                    fixed_length = request[0]          # dòng 2 là chiều dài có sẵn (nó cố định).
            elif len(request) == 2:     # Các thỏa mãn sẽ là các request.
                m1 = float(request[0])              # types
                m2 = int(request[1])                # quantity
                if not m1 in listRequest:
                    listRequest[m1] = m2
                else:
                    listRequest[m1] += m2
            else:
                break

        listRequest = {i: listRequest[i]
                       for i in sorted(listRequest, reverse=True)}
        types = [i for i in listRequest.keys()]
        numberOfTypes = [i for i in listRequest.values()]
        # print("Length: ", fixed_length, " - requests: ", numb_of_requests)
        # print(types)
        # print(numberOfTypes)

    # Tương tự như điền form
    fixed_length = float(fixed_length)
    if fixed_length < types[0]:
        fixed_length = types[0]
    return fixed_length, types, numberOfTypes


def get_cutting_instruction_by_uploading_file():
    # Giống với điền form.
    # Lấy dữ liêu cần thiết qua hàm method get_required_panels_by_uploading_file(), rồi cho vào hàm main để xử lý tiếp.
    return main(get_required_panels_by_uploading_file())
