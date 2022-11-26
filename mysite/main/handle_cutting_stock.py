from gurobipy import *

output_file = "main/static/output.txt"


def handle_uploaded_file(f):
    with open('main/static/upload/input.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def gurobi_solve(obj, A, x, numberOfType):  # min obj sub Ax >= b
    print("Gurobi Solve")
    model = Model()
    x_var = model.addVars(x, name="variable", vtype=GRB.INTEGER)
    model.setObjective(quicksum(obj[i] * x_var[i] for i in x), GRB.MINIMIZE)
    for i in range(0, len(A)):
        model.addConstr(quicksum(A[i][j] * x_var[j]
                                 for j in x) >= numberOfType[i])
    model.optimize()
    return model


def gurobi_show(model, output_data, pattern):
    output_data.write("Status gurobi: " + str(model.status) + "\n")
    cutting_instruction_list = []

    for i in range(len(model.getVars())):
        root = model.getVars()[i]
        if root.x > 0:
            # Thông tin của mỗi pattern
            pattern_info = {"number": root.x, "type": pattern[i]}
            pattern_dict = {}
            output_data.write(
                str(root.varName) + " = " +
                str(root.x) + "\t" + str(pattern[i]) + "\n"
            )

            # Json hoàn chỉnh để truy cập vào pattern
            pattern_dict["name"] = root.varName
            pattern_dict["value"] = pattern_info
            cutting_instruction_list.append(pattern_dict)

    optimal_value = model.objVal
    output_data.write("Optimal value gurobi = " + str(optimal_value) + "\n")
    return model.status, cutting_instruction_list, optimal_value


def solve(pattern: list, s: list, fixed_length: float, types: list, j: int, lowerBound: float):
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
        var.append("x" + str(i + 1))

    a = [[0 for i in range(0, len(pattern))] for j in range(0, int(lengthlist))]
    print(types)
    for i in range(0, len(pattern)):
        for j in range(0, len(pattern[i])):
            a[types.index(pattern[i][j])][i] += 1
    # Thể hiện chiều dài yêu cầu mà được cắt trong các patterns
    print("a[] = ", a)
    A = []
    for i in range(0, len(a)):
        A.append({})
        for j in range(0, len(var)):
            A[i][var[j]] = a[i][j]

    obj = {i: 1 for i in var}
    return A, obj, var


def main(func):
    output_data = open(output_file, "w")
    fixed_length, available_numb, types, numberOfTypes = func
    lowerBound = types[len(types) - 1]
    pattern = []
    solve(pattern, [], fixed_length, types, 0, lowerBound)
    print("Possible patterns: ", pattern)
    length_list = len(types)
    A, obj, var = get_frequency_of_types_in_patterns(types, pattern, length_list)
    print("\n\n")
    model = gurobi_solve(obj=obj, A=A, x=var, numberOfType=numberOfTypes)
    return gurobi_show(model, output_data, pattern)


def get_required_panels_by_filling(properties):
    required = []
    for k, v in properties.items():
        required.append(v[0])

    fixed_length = float(required[1])
    available_numb = int(required[2])
    listRequest = {}
    # 3 4 - 5 6 - 7 8
    start = 2
    for i in range(3, len(required)):
        if 2 * start >= len(required):
            break

        m1 = int(required[2 * start - 1])
        m2 = int(required[2 * start])
        if not m1 in listRequest:
            listRequest[m1] = m2
        else:
            listRequest[m1] += m2
        start += 1

    listRequest = {i: listRequest[i] for i in sorted(listRequest, reverse=True)}
    types = [i for i in listRequest.keys()]
    numberOfTypes = [i for i in listRequest.values()]
    return float(fixed_length), available_numb, types, numberOfTypes


def get_cutting_instruction_by_filling(properties):
    return main(get_required_panels_by_filling(properties))


def get_required_panels_by_uploading_file():
    # Mở file input do người dùng cung cấp
    with open("main/static/upload/input.txt") as file:
        listRequest = {}
        available_numb = 0
        while line := file.readline().rstrip():
            request = line.split()
            if len(request) == 1:
                if available_numb == 0:
                    available_numb = request[0]
                else:
                    fixed_length = request[0]
            elif len(request) == 2:
                m1 = float(request[0])
                m2 = int(request[1])
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
        print("Length: ", fixed_length, " - available: ", available_numb)
        print(types)
        print(numberOfTypes)
    return float(fixed_length), available_numb, types, numberOfTypes


def get_cutting_instruction_by_uploading_file():
    return main(get_required_panels_by_uploading_file())
