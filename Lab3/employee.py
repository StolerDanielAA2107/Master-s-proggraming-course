from io_strategy import FlaskIO

class Employee:
    def __init__(self, io_strategy: FlaskIO):
        self.io = io_strategy
        self.id = None
        self.name = ""
        self.age = 0

    def input_data(self):
        if self.io is None:
            raise ValueError("IO strategy is not set")
        self.name = self.io.input_field(self, 'name')
        self.age = int(self.io.input_field(self, 'age') or 0)

    def output_data(self):
        if self.io is None:
            raise ValueError("IO strategy is not set")
        output = {}
        self.io.output_field(self, 'name', output)
        self.io.output_field(self, 'age', output)
        self.io.output_field(self, 'id', output)
        return output