## Requirements

To run the muvid_test, you need the following software installed on your system:

- Python 3.x
- Flask
- NumPy
- Pandas
- scikit-learn
- SQLAlchemy

## Installation

1. Clone the repository to your local machine:

```shell
git clone <repository-url>

Install the required dependencies using pip:
pip install -r requirements.txt

The API will be accessible at http://localhost:5000.

# API Endpoints

The following endpoints are available in the API:
Get all employees
URL: /employees
Method: GET
Description: Retrieves a list of all employees.
Response: JSON object containing employee records.

Get an employee
URL: /employees/<employee_id>
Method: GET
Description: Retrieves information about a specific employee.
Response: JSON object containing the employee record.

Create an employee
URL: /employees
Method: POST
Description: Creates a new employee.
Request body: JSON object containing employee details (name, department, salary, hire_date).
Response: JSON object confirming the creation of the employee.

Update an employee
URL: /employees/<employee_id>
Method: PUT
Description: Updates information of an existing employee.
Request body: JSON object containing updated employee details (name, department, salary, hire_date).
Response: JSON object containing the updated employee record.

Delete an employee
URL: /employees/<employee_id>
Method: DELETE
Description: Deletes an employee.
Response: JSON object confirming the deletion of the employee.

Get all departments
URL: /departments
Method: GET
Description: Retrieves a list of all departments.
Response: JSON object containing department names.

Get employees in a department
URL: /departments/<department_name>
Method: GET
Description: Retrieves a list of employees in a specific department.
Response: JSON object containing employee records.

Get average salary of a department
URL: /average_salary/<department_name>
Method: GET
Description: Retrieves the average salary of employees in a specific department.
Response: JSON object containing the average salary.

Get top earners
URL: /top_earners
Method: GET
Description: Retrieves a list of the top 10 highest paid employees.
Response: JSON object containing employee records.

Get most recent hires
URL: /most_recent_hires
Method: GET
Description: Retrieves a list of the 10 most recent hires.
Response: JSON object containing employee records.

Predict salary
URL: /predict_salary
Method: POST
Description: Predicts the salary of an employee based on department and hire date.
Request body: JSON object containing department and hire date.
Response: JSON object containing the predicted salary.

Database
The muvid_test API uses a SQLite database to store employee records. The database file (employees.db) is located in the same directory as the code. You can modify the database connection settings in the app.py file if needed.


