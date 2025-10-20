from flask import request

class FlaskIO:
    def input_field(self, obj, field_name):
        return request.form.get(field_name, "")

    def output_field(self, obj, field_name, output_dict):
        value = getattr(obj, field_name)
        output_dict[field_name] = value

class IOStrategy:
    pass

class ConsoleIO(IOStrategy):
    def input_field(self, obj, field_name):
        return ""
    
    def output_field(self, obj, field_name):
        pass