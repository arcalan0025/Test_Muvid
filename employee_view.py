import logging
logger = logging.getLogger(__name__)
from flask import Flask, request, g, Blueprint
from flask import jsonify
from employee_model import EmployeeModel
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
import datetime
muvid_api = Blueprint('muvid_api', __name__)

# -------------------------------------------------------
# API Endpoints
# -------------------------------------------------------

# get all employees
@muvid_api.route('/employees', methods=['GET'])
def get_all_employees():
    '''
    Get all employees
    '''
    employees = EmployeeModel.get_all_employees()
    if employees:
        employees_list = []
        for employee in employees:
            employee_dict = {
                'id': employee.id,
                'name': employee.name,
                'department': employee.department,
                'salary': employee.salary,
                'hire_date': employee.hire_date.strftime('%Y-%m-%d')
            }
            employees_list.append(employee_dict)
        return jsonify(employees_list), 200
    else:
        return jsonify({'message': 'Employees not found'}), 404



# get one employee
@muvid_api.route('/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    '''
    Get one employee
    '''
    employee = EmployeeModel.get_one_employee(employee_id)
    if employee:
        employee_dict = {
            'id': employee.id,
            'name': employee.name,
            'department': employee.department,
            'salary': employee.salary,
            'hire_date': employee.hire_date.strftime('%Y-%m-%d')
        }
        return jsonify(employee_dict), 200
    else:
        return jsonify({'message': 'Employee not found'}), 404



# Add a new employee
@muvid_api.route('/employees', methods=['POST'])
def create_employee():
    '''
    Create an employee
    '''
    data = request.get_json()
    name = data.get('name')
    department = data.get('department')
    salary = data.get('salary')
    hire_date = data.get('hire_date')

    if not all([name, department, salary, hire_date]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        if isinstance(hire_date, datetime.date):
            hire_date = hire_date.strftime('%Y-%m-%d')  # Convert to string if it's a datetime.date object
        hire_date = datetime.datetime.strptime(hire_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid hire_date format. Expected format: YYYY-MM-DD'}), 400

    employee = EmployeeModel(name=name, department=department, salary=salary, hire_date=hire_date)
    db.session.add(employee)  # Add the employee object to the session

    # Commit the session to save the employee to the database
    db.session.commit()

    # Access the employee_id of the newly created employee
    employee_id = employee.id

    return jsonify({'message': 'Employee created successfully', 'id': employee_id}), 201
    


# Update an employee
@muvid_api.route('/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    '''
    Update an employee
    '''
    employee = EmployeeModel.get_one_employee(employee_id)
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    data = request.get_json()
    name = data.get('name')
    department = data.get('department')
    salary = data.get('salary')
    hire_date = data.get('hire_date')

    if not all([name, department, salary, hire_date]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        if isinstance(hire_date, datetime.date):
            hire_date = hire_date.strftime('%Y-%m-%d')  # Convert to string if it's a datetime.date object
        hire_date = datetime.datetime.strptime(hire_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid hire_date format. Expected format: YYYY-MM-DD'}), 400

    employee.name = name
    employee.department = department
    employee.salary = salary
    employee.hire_date = hire_date

    employee_dict = {
        'id': employee_id,
        'name': employee.name,
        'department': employee.department,
        'salary': employee.salary,
        'hire_date': employee.hire_date.strftime('%Y-%m-%d')
    }
    db.session.commit()
    return jsonify(employee_dict), 200


# Delete an employee
@muvid_api.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    '''
    Delete an employee
    '''
    employee = EmployeeModel.get_one_employee(employee_id)
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404
    EmployeeModel.delete_employee(employee_id)
    return jsonify({'message': 'Employee deleted successfully'}), 200


# Get all departments
@muvid_api.route('/departments', methods=['GET'])
def get_all_departments():
    '''
    Get all departments
    '''
    departments = EmployeeModel.get_all_departments()
    return jsonify(departments), 200


# Get all employees in a department
@muvid_api.route('/departments/<string:name>', methods=['GET'])
def get_employees_in_department(name):
    '''
    Get all employees in a department
    '''
    employees = EmployeeModel.get_employees_by_department(name)
    return jsonify(employees), 200


# Get average salary of a department
@muvid_api.route('/average_salary/<string:department>', methods=['GET'])
def get_average_salary_of_department(department):
    '''
    Get average salary of a department
    '''
    check_department = EmployeeModel.get_department_by_name(department)
    if not check_department:
        return jsonify({'message': 'Department not found'}), 404
    average_salary = EmployeeModel.get_average_salary_by_department(department)
    return jsonify(average_salary), 200


# Top 10 highest paid employees
@muvid_api.route('/top_earners', methods=['GET'])
def get_highest_paid_employees():
    '''
    Top 10 highest paid employees
    '''
    employees = EmployeeModel.get_top_10_earners()
    return jsonify(employees), 200


# Get most recent employees
@muvid_api.route('/most_recent_hires', methods=['GET'])
def get_recent_employees():
    '''
    Get most recent employees
    '''
    employees = EmployeeModel.get_last_10_hired()
    return jsonify(employees), 200