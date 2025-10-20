# employee.py
from io_strategy import IOStrategy

class Employee:
    def __init__(self, io_strategy: IOStrategy):
        self.io = io_strategy
        self.name = ""
        self.age = 0

    def input_data(self):
        self.name = self.io.input_field(self, 'name')
        self.age = int(self.io.input_field(self, 'age'))

    def output_data(self):
        self.io.output_field(self, 'name')
        self.io.output_field(self, 'age')