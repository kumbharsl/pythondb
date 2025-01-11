# from flask import Flask, jsonify, request
# from flasgger import Swagger, swag_from
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)

# # Swagger configuration
# template = {
#     "swagger": "2.0",
#     "info": {
#         "title": "Employee Registration API",
#         "description": "API for employee registration and management",
#         "version": "1.0.0"
#     }
# }

# swagger_config = {
#     "headers": [],
#     "specs": [{
#         "endpoint": 'apispec',
#         "route": '/apispec.json',
#         "rule_filter": lambda rule: True,
#         "model_filter": lambda tag: True,
#     }],
#     "static_url_path": "/flasgger_static",
#     "swagger_ui": True,
#     "specs_route": "/swagger/"
# }

# swagger = Swagger(app, template=template, config=swagger_config)

# # Mock database
# employees = []

# @app.route('/api/register', methods=['POST'])
# @swag_from({
#     'tags': ['Employee'],
#     'summary': 'Register a new employee',
#     'parameters': [{
#         'name': 'body',
#         'in': 'body',
#         'required': True,
#         'schema': {
#             'type': 'object',
#             'properties': {
#                 'username': {
#                     'type': 'string',
#                     'example': 'john_doe'
#                 },
#                 'email': {
#                     'type': 'string',
#                     'example': 'john@example.com'
#                 },
#                 'password': {
#                     'type': 'string',
#                     'example': 'secretpassword'
#                 },
#                 'full_name': {
#                     'type': 'string',
#                     'example': 'John Doe'
#                 },
#                 'department': {
#                     'type': 'string',
#                     'example': 'IT'
#                 }
#             },
#             'required': ['username', 'email', 'password', 'full_name', 'department']
#         }
#     }],
#     'responses': {
#         201: {
#             'description': 'Employee registered successfully'
#         },
#         400: {
#             'description': 'Missing required fields'
#         }
#     }
# })
# def register():
#     data = request.get_json()
    
#     # Check if all required fields are present
#     required_fields = ['username', 'email', 'password', 'full_name', 'department']
#     for field in required_fields:
#         if field not in data:
#             return jsonify({
#                 'message': f'Missing required field: {field}',
#                 'required_fields': required_fields
#             }), 400
    
#     # Check if email already exists
#     if any(emp['email'] == data['email'] for emp in employees):
#         return jsonify({'message': 'Email already registered'}), 400
    
#     # Create new employee
#     new_employee = {
#         'id': len(employees) + 1,
#         'username': data['username'],
#         'email': data['email'],
#         'password': generate_password_hash(data['password']),
#         'full_name': data['full_name'],
#         'department': data['department']
#     }
#     employees.append(new_employee)
    
#     return jsonify({
#         'message': 'Employee registered successfully',
#         'employee_id': new_employee['id']
#     }), 201

# @app.route('/api/employees', methods=['GET'])
# @swag_from({
#     'tags': ['Employee'],
#     'summary': 'Get all employees',
#     'responses': {
#         200: {
#             'description': 'List of all employees'
#         }
#     }
# })
# def get_employees():
#     # Return employees without password field
#     safe_employees = [
#         {k: v for k, v in emp.items() if k != 'password'}
#         for emp in employees
#     ]
#     return jsonify(safe_employees)

# @app.route('/api/employees/<int:employee_id>', methods=['PUT'])
# @swag_from({
#     'tags': ['Employee'],
#     'summary': 'Update an employee',
#     'parameters': [
#         {
#             'name': 'employee_id',
#             'in': 'path',
#             'type': 'integer',
#             'required': True,
#             'description': 'ID of the employee to update'
#         },
#         {
#             'name': 'body',
#             'in': 'body',
#             'required': True,
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'username': {
#                         'type': 'string',
#                         'example': 'john_doe_updated'
#                     },
#                     'email': {
#                         'type': 'string',
#                         'example': 'john_updated@example.com'
#                     },
#                     'full_name': {
#                         'type': 'string',
#                         'example': 'John Doe Updated'
#                     },
#                     'department': {
#                         'type': 'string',
#                         'example': 'HR'
#                     },
#                     'password': {
#                         'type': 'string',
#                         'example': 'newpassword'
#                     }
#                 }
#             }
#         }
#     ],
#     'responses': {
#         200: {
#             'description': 'Employee updated successfully'
#         },
#         404: {
#             'description': 'Employee not found'
#         }
#     }
# })
# def update_employee(employee_id):
#     data = request.get_json()
    
#     # Find employee by ID
#     employee = next((emp for emp in employees if emp['id'] == employee_id), None)
#     if not employee:
#         return jsonify({'message': 'Employee not found'}), 404
    
#     # Check if updating email and if it already exists for another employee
#     if 'email' in data and data['email'] != employee['email']:
#         if any(emp['email'] == data['email'] for emp in employees if emp['id'] != employee_id):
#             return jsonify({'message': 'Email already registered to another employee'}), 400
    
#     # Update employee fields
#     updateable_fields = ['username', 'email', 'full_name', 'department']
#     for field in updateable_fields:
#         if field in data:
#             employee[field] = data[field]
    
#     # Update password if provided
#     if 'password' in data:
#         employee['password'] = generate_password_hash(data['password'])
    
#     return jsonify({
#         'message': 'Employee updated successfully',
#         'employee': {k: v for k, v in employee.items() if k != 'password'}
#     })

# @app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
# @swag_from({
#     'tags': ['Employee'],
#     'summary': 'Delete an employee',
#     'parameters': [
#         {
#             'name': 'employee_id',
#             'in': 'path',
#             'type': 'integer',
#             'required': True,
#             'description': 'ID of the employee to delete'
#         }
#     ],
#     'responses': {
#         200: {
#             'description': 'Employee deleted successfully'
#         },
#         404: {
#             'description': 'Employee not found'
#         }
#     }
# })
# def delete_employee(employee_id):
#     # Find employee by ID
#     employee = next((emp for emp in employees if emp['id'] == employee_id), None)
#     if not employee:
#         return jsonify({'message': 'Employee not found'}), 404
    
#     # Remove employee from list
#     employees.remove(employee)
    
#     return jsonify({
#         'message': 'Employee deleted successfully',
#         'deleted_employee_id': employee_id
#     })

# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from werkzeug.security import generate_password_hash, check_password_hash
import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime

app = Flask(__name__)

# Enable logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"D:\New folder (7)\pythonb-57ec6-firebase-adminsdk-7wagn-3802d6b97f.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Home route
@app.route('/')
def home():
    return jsonify({
        'message': 'Welcome to Employee Registration API',
        'documentation': '/swagger/',
        'endpoints': {
            'register': '/api/register',
            'get_all_employees': '/api/employees',
            'update_employee': '/api/employees/<employee_id>',
            'delete_employee': '/api/employees/<employee_id>'
        }
    })

# Swagger configuration remains the same as your original code
template = {
    "swagger": "2.0",
    "info": {
        "title": "Employee Registration API",
        "description": "API for employee registration and management with Firebase",
        "version": "1.0.0"
    }
}

swagger_config = {
    "headers": [],
    "specs": [{
        "endpoint": 'apispec',
        "route": '/apispec.json',
        "rule_filter": lambda rule: True,
        "model_filter": lambda tag: True,
    }],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/"
}

swagger = Swagger(app, template=template, config=swagger_config)

@app.route('/api/register', methods=['POST'])
@swag_from({
    'tags': ['Employee'],
    'summary': 'Register a new employee',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'username': {'type': 'string', 'example': 'john_doe'},
                'email': {'type': 'string', 'example': 'john@example.com'},
                'password': {'type': 'string', 'example': 'secretpassword'},
                'full_name': {'type': 'string', 'example': 'John Doe'},
                'department': {'type': 'string', 'example': 'IT'}
            },
            'required': ['username', 'email', 'password', 'full_name', 'department']
        }
    }]
})
def register():
    try:
        # Verify JSON data
        if not request.is_json:
            return jsonify({'message': 'Missing JSON in request'}), 400
            
        data = request.get_json()
        print("Received data:", data)  # Debug print
        
        # Check required fields
        required_fields = ['username', 'email', 'password', 'full_name', 'department']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'message': f'Missing required fields: {", ".join(missing_fields)}',
                'required_fields': required_fields
            }), 400

        try:
            # Check if email already exists
            users_ref = db.collection('employees')
            print("Checking for existing email:", data['email'])  # Debug print
            existing_user = users_ref.where('email', '==', data['email']).limit(1).get()
            if len(list(existing_user)) > 0:
                return jsonify({'message': 'Email already registered'}), 400

            # Create new employee document
            new_employee = {
                'username': data['username'],
                'email': data['email'],
                'password': generate_password_hash(data['password']),
                'full_name': data['full_name'],
                'department': data['department'],
                'created_at': firestore.SERVER_TIMESTAMP,
                'updated_at': firestore.SERVER_TIMESTAMP
            }
            
            print("Attempting to add new employee to Firestore")  # Debug print
            # Add to Firestore
            doc_ref = users_ref.add(new_employee)
            
            return jsonify({
                'message': 'Employee registered successfully',
                'employee_id': doc_ref[1].id
            }), 201
            
        except Exception as firebase_error:
            print(f"Firebase operation error: {str(firebase_error)}")  # Debug print
            return jsonify({
                'message': 'Database operation failed',
                'error': str(firebase_error)
            }), 500
            
    except Exception as e:
        print(f"General error: {str(e)}")  # Debug print
        return jsonify({
            'message': 'Server error occurred',
            'error': str(e)
        }), 500

@app.route('/api/employees', methods=['GET'])
@swag_from({
    'tags': ['Employee'],
    'summary': 'Get all employees'
})
def get_employees():
    try:
        employees_ref = db.collection('employees')
        docs = employees_ref.stream()
        
        employees_list = []
        for doc in docs:
            employee_data = doc.to_dict()
            employee_data['id'] = doc.id
            # Remove password from response
            employee_data.pop('password', None)
            employees_list.append(employee_data)
            
        return jsonify(employees_list), 200
        
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@app.route('/api/employees/<employee_id>', methods=['PUT'])
@swag_from({
    'tags': ['Employee'],
    'summary': 'Update an employee',
    'parameters': [
        {
            'name': 'employee_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the employee to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string'},
                    'email': {'type': 'string'},
                    'full_name': {'type': 'string'},
                    'department': {'type': 'string'},
                    'password': {'type': 'string'}
                }
            }
        }
    ]
})
def update_employee(employee_id):
    try:
        data = request.get_json()
        employee_ref = db.collection('employees').document(employee_id)
        employee = employee_ref.get()
        
        if not employee.exists:
            return jsonify({'message': 'Employee not found'}), 404
            
        # Check if updating email and if it already exists
        if 'email' in data and data['email'] != employee.to_dict()['email']:
            existing_email = db.collection('employees').where('email', '==', data['email']).get()
            if len(list(existing_email)) > 0:
                return jsonify({'message': 'Email already registered to another employee'}), 400
        
        update_data = {}
        updateable_fields = ['username', 'email', 'full_name', 'department']
        for field in updateable_fields:
            if field in data:
                update_data[field] = data[field]
                
        if 'password' in data:
            update_data['password'] = generate_password_hash(data['password'])
            
        update_data['updated_at'] = datetime.now()
        
        # Update document
        employee_ref.update(update_data)
        
        # Get updated employee data
        updated_employee = employee_ref.get().to_dict()
        updated_employee.pop('password', None)
        updated_employee['id'] = employee_id
        
        return jsonify({
            'message': 'Employee updated successfully',
            'employee': updated_employee
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

@app.route('/api/employees/<employee_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Employee'],
    'summary': 'Delete an employee',
    'parameters': [
        {
            'name': 'employee_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'ID of the employee to delete'
        }
    ]
})
def delete_employee(employee_id):
    try:
        employee_ref = db.collection('employees').document(employee_id)
        employee = employee_ref.get()
        
        if not employee.exists:
            return jsonify({'message': 'Employee not found'}), 404
            
        # Delete document
        employee_ref.delete()
        
        return jsonify({
            'message': 'Employee deleted successfully',
            'deleted_employee_id': employee_id
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)