from flask import Flask, request, render_template, redirect, url_for, flash
from company import Company
from io_strategy import FlaskIO
import os

app = Flask(__name__, 
            template_folder=os.path.join('app', 'templates'),
            static_folder=os.path.join('app', 'static'))
app.secret_key = 'supersecretkey'

os.makedirs('data', exist_ok=True)
os.makedirs(os.path.join('app', 'templates'), exist_ok=True)
os.makedirs(os.path.join('app', 'static', 'css'), exist_ok=True)
os.makedirs(os.path.join('app', 'static', 'js'), exist_ok=True)

company = Company(FlaskIO())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        emp_type = request.form.get('emp_type')
        if emp_type:
            message = company.add_employee(emp_type)
            flash(message)
            return redirect(url_for('employee_list'))
    return render_template('add.html')

@app.route('/edit/<emp_id>', methods=['GET', 'POST'])
def edit_employee(emp_id):
    emp = company.storage.get_by_id(emp_id)
    if not emp:
        flash("Employee not found.")
        return redirect(url_for('employee_list'))
    
    if request.method == 'POST':
        message = company.edit_employee(emp_id)
        flash(message)
        return redirect(url_for('employee_list'))
    
    return render_template('edit.html', emp=emp.output_data(), emp_type=emp.__class__.__name__)

@app.route('/delete/<emp_id>')
def delete_employee(emp_id):
    message = company.delete_employee(emp_id)
    flash(message)
    return redirect(url_for('employee_list'))

@app.route('/list')
def employee_list():
    employees = company.get_employee_list()
    return render_template('list.html', employees=employees)

@app.route('/save', methods=['GET', 'POST'])
def save_to_file():
    if request.method == 'POST':
        filename = request.form.get('filename')
        if filename:
            message = company.save_to_file(filename)
            flash(message)
            return redirect(url_for('index'))
    return render_template('save.html')

@app.route('/load', methods=['GET', 'POST'])
def load_from_file():
    if request.method == 'POST':
        filename = request.form.get('filename')
        if filename:
            message = company.load_from_file(filename)
            flash(message)
            return redirect(url_for('index'))
    return render_template('load.html')

@app.route('/clear')
def clear_list():
    message = company.clear_list()
    flash(message)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)