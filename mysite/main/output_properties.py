class output_properties:
    def __init__(self, *args):
        if len(args) == 3:
            self.status = args[0]
            self.cutting_instruction_list = args[1]
            self.optimal_value = args[2]

    def get_status(self):
        return self.status

    def get_cutting_instruction_list(self):
        return self.cutting_instruction_list

    def get_optimal_value(self):
        return self.optimal_value

    def set_status(self, s):
        self.status = s

    def set_cutting_instruction_list(self, c):
        self.cutting_instruction_list = c

    def set_optimal_value(self, o):
        self.optimal_value = o
