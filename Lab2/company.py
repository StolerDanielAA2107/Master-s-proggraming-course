from employee import Employee
from manager import Manager
from director import Director
from storage_strategy import PickleStorage

class Company:
    def __init__(self, io_strategy):
        self.io = io_strategy
        self.storage = PickleStorage()

    def add_employee(self, emp_type, input_data=None):
        if emp_type == 'Employee':
            emp = Employee(self.io)
        elif emp_type == 'Manager':
            emp = Manager(self.io)
        elif emp_type == 'Director':
            emp = Director(self.io)
        else:
            return "Неправильный выбор"
        emp.input_data()
        self.storage.add(emp)
        return "Сотрудник добавлен"

    def edit_employee(self, emp_id):
        emp = self.storage.get_by_id(emp_id)
        if emp:
            emp.input_data()
            self.storage.update_by_id(emp_id, emp)
            return "Сотрудник изменён"
        return "Неправильный ID."

    def delete_employee(self, emp_id):
        if self.storage.get_by_id(emp_id):
            self.storage.delete_by_id(emp_id)
            return "Сотрудник удалён"
        return "Неправильный ID."

    def get_employee_list(self):
        employees = self.storage.get_all()
        output_list = []
        for emp in employees:
            output = emp.output_data()
            output['type'] = emp.__class__.__name__
            output_list.append(output)
        return output_list

    def save_to_file(self, filename):
        self.storage.save(filename)
        return "Сохранено в файл"

    def load_from_file(self, filename):
        try:
            self.storage.load(filename)
            return "Загружено из файла"
        except FileNotFoundError:
            return "Файл не найден"
        except Exception as e:
            return f"Ошибка загрузки: {e}"

    def clear_list(self):
        self.storage.clear()
        return "Список очищен"