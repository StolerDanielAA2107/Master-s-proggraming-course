# manager.py
from employee import Employee
from io_strategy import IOStrategy

class Manager(Employee):
    def __init__(self, io_strategy: IOStrategy):
        super().__init__(io_strategy)
        self.department = ""

    def input_data(self):
        super().input_data()
        self.department = self.io.input_field(self, 'department')

    def output_data(self):
        super().output_data()
        self.io.output_field(self, 'department')