# company.py
from employee import Employee
from manager import Manager
from director import Director
from io_strategy import ConsoleIO
from storage_strategy import PickleStorage

class Company:
    def __init__(self):
        self.employees = []
        self.storage = PickleStorage()

    def add_employee(self):
        print("Choose type: 1 - Employee, 2 - Manager, 3 - Director")
        choice = int(input("Enter choice: "))
        io = ConsoleIO()
        if choice == 1:
            emp = Employee(io)
        elif choice == 2:
            emp = Manager(io)
        elif choice == 3:
            emp = Director(io)
        else:
            print("Invalid choice")
            return
        emp.input_data()
        self.employees.append(emp)
        print("Employee added.")

    def edit_employee(self):
        if not self.employees:
            print("No employees to edit.")
            return
        self.print_list()
        index = int(input("Enter index to edit (1-based): ")) - 1
        if 0 <= index < len(self.employees):
            self.employees[index].input_data()
            print("Employee edited.")
        else:
            print("Invalid index.")

    def delete_employee(self):
        if not self.employees:
            print("No employees to delete.")
            return
        self.print_list()
        index = int(input("Enter index to delete (1-based): ")) - 1
        if 0 <= index < len(self.employees):
            del self.employees[index]
            print("Employee deleted.")
        else:
            print("Invalid index.")

    def print_list(self):
        if not self.employees:
            print("No employees.")
            return
        for i, emp in enumerate(self.employees, start=1):
            print(f"Employee {i} ({emp.__class__.__name__}):")
            emp.output_data()
            print("---")

    def save_to_file(self):
        filename = input("Enter filename to save: ")
        self.storage.save(self.employees, filename)
        print("Saved to file.")

    def load_from_file(self):
        filename = input("Enter filename to load: ")
        try:
            self.employees = self.storage.load(filename)
            print("Loaded from file.")
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"Error loading: {e}")

    def clear_list(self):
        self.employees.clear()
        print("List cleared.")