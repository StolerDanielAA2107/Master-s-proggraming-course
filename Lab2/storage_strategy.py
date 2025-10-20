import pickle
import uuid

class StorageStrategy:
    def add(self, employee):
        raise NotImplementedError

    def get_all(self):
        raise NotImplementedError

    def get_by_id(self, emp_id):
        raise NotImplementedError

    def update_by_id(self, emp_id, employee):
        raise NotImplementedError

    def delete_by_id(self, emp_id):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def save(self, filename):
        raise NotImplementedError

    def load(self, filename):
        raise NotImplementedError

class PickleStorage(StorageStrategy):
    def __init__(self):
        self._employees = {}  

    def add(self, employee):
        if not employee.id:
            employee.id = str(uuid.uuid4())
        self._employees[employee.id] = employee  

    def get_all(self):
        return list(self._employees.values())  

    def get_by_id(self, emp_id):
        return self._employees.get(emp_id)

    def update_by_id(self, emp_id, employee):
        if emp_id in self._employees:
            employee.id = emp_id  
            self._employees[emp_id] = employee

    def delete_by_id(self, emp_id):
        if emp_id in self._employees:
            del self._employees[emp_id]

    def clear(self):
        self._employees.clear()

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self._employees, f) 

    def load(self, filename):
        with open(filename, 'rb') as f:
            self._employees = pickle.load(f)  