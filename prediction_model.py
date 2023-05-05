from flask import Flask, request, g, Blueprint
from flask import jsonify
from employee_model import EmployeeModel
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
muvid_api_prediction = Blueprint('muvid_api_prediction', __name__)
from datetime import timedelta
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from employee_model import EmployeeModel
from sklearn.preprocessing import OneHotEncoder


# Connect to the SQLite database and load the dataset
employees = EmployeeModel.get_all_employees()
employees = [(employee.department, employee.hire_date, employee.salary) for employee in employees]
df = pd.DataFrame(employees, columns=['department', 'hire_date', 'salary'])
df['hire_date'] = (df['hire_date'] - df['hire_date'].min()).dt.days

department_encoder = LabelEncoder()
df['department'] = department_encoder.fit_transform(df['department'])

onehot_encoder = OneHotEncoder(sparse=False)
department_encoded = onehot_encoder.fit_transform(df[['department']])
df_encoded = pd.concat([df.drop('department', axis=1), pd.DataFrame(department_encoded)], axis=1)

X = df_encoded.drop('salary', axis=1)
y = df_encoded['salary']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# Convert feature names to strings
X_train.columns = X_train.columns.astype(str)
X_test.columns = X_test.columns.astype(str)

model = LinearRegression()
model.fit(X_train, y_train)


# Predict the salary
@muvid_api_prediction.route('/predict_salary', methods=['POST'])
def predict_salary():
    data = request.get_json()
    department = data['department']
    hire_date = data['hire_date']
    
    # Preprocess the input data
    hire_date = datetime.strptime(hire_date, "%Y-%m-%d")
    min_hire_date_str = str(df['hire_date'].min())
    
    if pd.isnull(df['hire_date'].min()) or min_hire_date_str == '0':
        return jsonify({'error': 'No hire date data available.'})
    else:
        min_hire_date = datetime.strptime(min_hire_date_str, "%Y-%m-%d")
        # Calculating experience range
        hire_date_diff = hire_date - min_hire_date
        hire_date_diff_days = hire_date_diff / timedelta(days=1)
        
        department_encoded = department_encoder.transform([department])
        department_encoded = onehot_encoder.transform([[department_encoded]])
        input_data = pd.DataFrame([[hire_date_diff_days]], columns=['hire_date'])
        input_data_encoded = pd.concat([input_data, pd.DataFrame(department_encoded)], axis=1)
        
        # Make the salary prediction
        salary_prediction = model.predict(input_data_encoded)[0]
        
        return jsonify({'salary': salary_prediction})
