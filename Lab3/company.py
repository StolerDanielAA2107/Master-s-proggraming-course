from employee import Employee
from manager import Manager
from director import Director
from storage import SQLiteStorage

class Company:
    def __init__(self, io_strategy):
        self.io = io_strategy
        self.storage = SQLiteStorage()

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
            original_io = emp.io
            emp.io = self.io
            emp.input_data()
            emp.io = original_io
            
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
        saved_path = self.storage.save(filename)
        return f"Сохранено в файл: {saved_path}"

    def load_from_file(self, filename):
        try:
            success = self.storage.load(filename)
            if success:
                return f"Данные успешно загружены из файла {filename}"
            else:
                return f"Не удалось загрузить данные из файла {filename}"
        except FileNotFoundError as e:
            return f"Файл не найден: {str(e)}"
        except Exception as e:
            return f"Ошибка загрузки: {str(e)}"

    def clear_list(self):
        self.storage.clear()
        return "Список очищен"