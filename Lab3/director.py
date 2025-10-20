from employee import Employee
from io_strategy import FlaskIO

class Director(Employee):
    def __init__(self, io_strategy: FlaskIO):
        super().__init__(io_strategy)
        self.title = ""

    def input_data(self):
        if self.io is None:
            raise ValueError("IO strategy is not set")
        super().input_data()
        self.title = self.io.input_field(self, 'title')

    def output_data(self):
        if self.io is None:
            raise ValueError("IO strategy is not set")
        output = super().output_data()
        self.io.output_field(self, 'title', output)
        return output