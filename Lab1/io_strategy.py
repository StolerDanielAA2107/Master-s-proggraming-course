# io_strategy.py

class IOStrategy:
    def input_field(self, obj, field_name):
        raise NotImplementedError

    def output_field(self, obj, field_name):
        raise NotImplementedError

class ConsoleIO(IOStrategy):
    def input_field(self, obj, field_name):
        return input(f"Enter {field_name}: ")

    def output_field(self, obj, field_name):
        value = getattr(obj, field_name)
        print(f"{field_name.capitalize()}: {value}")