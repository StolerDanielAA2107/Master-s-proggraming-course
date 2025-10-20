import sqlite3
import uuid
import os
from .io_strategy import FlaskIO

class SQLiteStorage:
    def __init__(self, db_path='data/company.db'):
        os.makedirs('data', exist_ok=True)
        self.db_path = db_path
        self.io = FlaskIO()
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    id TEXT PRIMARY KEY,
                    type TEXT NOT NULL,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    department TEXT,
                    title TEXT
                )
            ''')
            conn.commit()

    def add(self, employee):
        if not employee.id:
            employee.id = str(uuid.uuid4())
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO employees (id, type, name, age, department, title)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                employee.id,
                employee.__class__.__name__,
                employee.name,
                employee.age,
                getattr(employee, 'department', None),
                getattr(employee, 'title', None)
            ))
            conn.commit()

    def get_all(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM employees')
            rows = cursor.fetchall()
            
            employees = []
            for row in rows:
                emp_id, emp_type, name, age, department, title = row
                
                if emp_type == 'Employee':
                    from employee import Employee
                    emp = Employee(self.io)
                elif emp_type == 'Manager':
                    from manager import Manager
                    emp = Manager(self.io)
                elif emp_type == 'Director':
                    from director import Director
                    emp = Director(self.io)
                else:
                    continue
                
                emp.id = emp_id
                emp.name = name
                emp.age = age
                if hasattr(emp, 'department'):
                    emp.department = department
                if hasattr(emp, 'title'):
                    emp.title = title
                
                employees.append(emp)
            
            return employees

    def get_by_id(self, emp_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM employees WHERE id = ?', (emp_id,))
            row = cursor.fetchone()
            
            if row:
                emp_id, emp_type, name, age, department, title = row
                
                if emp_type == 'Employee':
                    from employee import Employee
                    emp = Employee(self.io)
                elif emp_type == 'Manager':
                    from manager import Manager
                    emp = Manager(self.io)
                elif emp_type == 'Director':
                    from director import Director
                    emp = Director(self.io)
                else:
                    return None
                
                emp.id = emp_id
                emp.name = name
                emp.age = age
                if hasattr(emp, 'department'):
                    emp.department = department
                if hasattr(emp, 'title'):
                    emp.title = title
                
                return emp
            return None

    def update_by_id(self, emp_id, employee):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE employees 
                SET name = ?, age = ?, department = ?, title = ?
                WHERE id = ?
            ''', (
                employee.name,
                employee.age,
                getattr(employee, 'department', None),
                getattr(employee, 'title', None),
                emp_id
            ))
            conn.commit()

    def delete_by_id(self, emp_id):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM employees WHERE id = ?', (emp_id,))
            conn.commit()

    def clear(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM employees')
            conn.commit()

    def _ensure_data_dir(self, filename):
        """Обеспечивает, что файл сохраняется в папку data"""
        # Если путь уже содержит data/, оставляем как есть
        if filename.startswith('data/'):
            return filename
        
        # Если указан абсолютный путь, проверяем не ведет ли он в data
        if os.path.isabs(filename):
            data_dir = os.path.abspath('data')
            file_dir = os.path.dirname(filename)
            if file_dir == data_dir:
                return filename
        
        # Во всех остальных случаях сохраняем в data/
        return os.path.join('data', filename)

    def save(self, filename):
        """Сохраняет данные в файл, автоматически в папку data"""
        import pickle
        
        # Обеспечиваем сохранение в папку data
        file_path = self._ensure_data_dir(filename)
        
        # Создаем папку data если её нет
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        employees = self.get_all()
        with open(file_path, 'wb') as f:
            pickle.dump(employees, f)
        
        print(f"Данные сохранены в: {file_path}")
        return file_path

    def _find_file(self, filename):
        """Ищет файл в разных местах по имени, с приоритетом папки data"""
        # Сначала ищем в папке data
        data_path = os.path.join('data', filename)
        if os.path.exists(data_path) and os.path.isfile(data_path):
            print(f"Файл найден в data/: {data_path}")
            return data_path
        
        # Затем ищем по прямому пути
        if os.path.exists(filename) and os.path.isfile(filename):
            print(f"Файл найден по прямому пути: {filename}")
            return filename
        
        # Ищем файлы с разными расширениями в data
        base_name = os.path.splitext(filename)[0]
        extensions = ['.pkl', '.pickle', '.txt', '.dat']
        
        for ext in extensions:
            data_ext_path = os.path.join('data', base_name + ext)
            if os.path.exists(data_ext_path) and os.path.isfile(data_ext_path):
                print(f"Файл найден в data/ с расширением {ext}: {data_ext_path}")
                return data_ext_path
        
        # Ищем файлы с разными расширениями в текущей директории
        for ext in extensions:
            ext_path = base_name + ext
            if os.path.exists(ext_path) and os.path.isfile(ext_path):
                print(f"Файл найден с расширением {ext}: {ext_path}")
                return ext_path
        
        print(f"Файл '{filename}' не найден")
        return None

    def _create_compatibility_classes(self):
        """Создает классы для совместимости с первой версией"""
        class ConsoleIO:
            """Класс для совместимости с первой версией"""
            def input_field(self, obj, field_name):
                return ""
            
            def output_field(self, obj, field_name):
                pass

        class IOStrategy:
            """Абстрактный класс для совместимости"""
            pass

        return {'ConsoleIO': ConsoleIO, 'IOStrategy': IOStrategy}

    def load(self, filename):
        """Загружает данные из файла, обеспечивает совместимость с первой версией"""
        try:
            file_path = self._find_file(filename)
            
            if not file_path:
                raise FileNotFoundError(f"Файл '{filename}' не найден")
            
            print(f"Загружаем данные из: {file_path}")
            
            import pickle
            import sys
            
            # Создаем классы для совместимости
            compatibility_classes = self._create_compatibility_classes()
            
            # Временно добавляем классы в модуль io_strategy для pickle
            original_consoleio = getattr(sys.modules['io_strategy'], 'ConsoleIO', None)
            original_iostrategy = getattr(sys.modules['io_strategy'], 'IOStrategy', None)
            
            # Подменяем классы для загрузки
            sys.modules['io_strategy'].ConsoleIO = compatibility_classes['ConsoleIO']
            sys.modules['io_strategy'].IOStrategy = compatibility_classes['IOStrategy']
            
            try:
                with open(file_path, 'rb') as f:
                    employees = pickle.load(f)
            finally:
                # Восстанавливаем оригинальные классы
                if original_consoleio is not None:
                    sys.modules['io_strategy'].ConsoleIO = original_consoleio
                else:
                    delattr(sys.modules['io_strategy'], 'ConsoleIO')
                    
                if original_iostrategy is not None:
                    sys.modules['io_strategy'].IOStrategy = original_iostrategy
                else:
                    delattr(sys.modules['io_strategy'], 'IOStrategy')
            
            self.clear()
            for emp in employees:
                # Заменяем старую стратегию ввода-вывода на новую
                emp.io = self.io
                
                # Генерируем ID если его нет (для совместимости с первой версией)
                if not hasattr(emp, 'id') or emp.id is None:
                    emp.id = str(uuid.uuid4())
                    print(f"Сгенерирован ID для сотрудника: {emp.name} -> {emp.id}")
                
                self.add(emp)
                
            return True
            
        except FileNotFoundError as e:
            print(f"Ошибка: {e}")
            raise
        except Exception as e:
            print(f"Ошибка загрузки из файла {filename}: {e}")
            raise