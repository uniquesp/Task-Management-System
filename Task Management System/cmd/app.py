import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from internal.repository import InitializeDatabase, TaskStatus
from internal.pkg.specs import ValidateRegistrationPayload
from internal.service.service import CreateTask, DeleteTask, FetchUserTasks, UpdateTask, UserRegistration, UserLogin
from flask import Flask, request, jsonify, g
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)

# Set the JWT secret key and token location
app.config['JWT_SECRET_KEY'] = 'YOUR_SECRET_KEY'  # Change this to a more secure key
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600  # Token expiration time in seconds

# Initialize JWTManager
jwt = JWTManager(app)


@app.before_request
def setup_database():
    g.db_session = InitializeDatabase()

@app.teardown_appcontext
def teardown_database(exception=None):
    session = g.pop('db_session', None)
    if session:
        session.close()

@app.route('/', methods=['GET'])
def home():
    return "Welcome to Home | Task Management System @Sakshi Pharande"


@app.route('/api/register', methods=['POST'])
def registeruser():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not ValidateRegistrationPayload(username, password):
        return jsonify({'message': 'Invalid registration data'}), 400
    
    database = g.get('db_session')
    if database is None:
        return jsonify({'message': 'Database not available'}), 500
    
    result = UserRegistration(database, username, password)
    
    if result:
        return jsonify({
            'message': 'User registered successfully!',
            'username': username,
            'password': password
        }), 201
    else:
        return jsonify({'message': 'Invalid registration request'}), 400


@app.route('/api/login', methods=['POST'])
def loginuser():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not ValidateRegistrationPayload(username, password):
        return jsonify({'message': 'Invalid login data'}), 400
    
    database = g.get('db_session')
    if database is None:
        return jsonify({'message': 'Database not available'}), 500
    
    token = UserLogin(database, username, password)

    if token:
        return jsonify({
            'message': 'User logged in successfully!',
            'token': token,
        }), 201
    else:
        return jsonify({'message': 'Invalid login request'}), 400


@app.route('/api/tasks', methods=['POST'])
@jwt_required()
def addtask():
    # Get the user_id from the JWT identity
    current_user = get_jwt_identity()  # This should give you the user's identity
    user_id = current_user['id']  # Extract user ID from the identity
    # Check if user_id is valid
    if not user_id:
        return jsonify({"message": "Invalid or expired token"}), 401

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    status = data.get('status', TaskStatus.TODO.value)
    priority = data.get('priority')
    due_date = data.get('due_date')

    # Validate required fields
    if not title or not priority:
        return jsonify({'message': 'Title and priority are required'}), 400

    database = g.get('db_session')
    if database is None:
        return jsonify({'message': 'Database not available'}), 500

    result = CreateTask(database, title, description, status, priority, due_date, user_id)

    if result:
        return jsonify({
            'message': 'Task created successfully!',
            'task': result.to_dict()  # Call the to_dict method
        }), 201
    else:
        return jsonify({'message': 'Task creation failed'}), 400



@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def gettask():
    # Get the user_id from the JWT identity
    current_user = get_jwt_identity()
    user_id = current_user['id']

    # Check if user_id is valid
    if not user_id:
        return jsonify({"message": "Invalid or expired token"}), 401

    database = g.get('db_session')
    if database is None:
        return jsonify({'message': 'Database not available'}), 500

    # Get query parameters for filtering and searching
    status = request.args.get('status')
    priority = request.args.get('priority')
    due_date = request.args.get('due_date')
    search_query = request.args.get('search')

    # Fetch tasks based on filters and search query
    tasks = FetchUserTasks(database, user_id, status, priority, due_date, search_query)

    if tasks is not None:
        return jsonify({
            'message': 'Tasks retrieved successfully!',
            'tasks': [task.to_dict() for task in tasks]  # Assuming to_dict() method exists
        }), 200
    else:
        return jsonify({'message': 'No tasks found or retrieval failed'}), 404


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def updatetask(task_id):
    current_user = get_jwt_identity()
    user_id = current_user['id']

    # Check if user_id is valid
    if not user_id:
        return jsonify({"message": "Invalid or expired token"}), 401

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    status = data.get('status')
    priority = data.get('priority')
    due_date = data.get('due_date')

    # Validate required fields
    if not title or not priority:
        return jsonify({'message': 'Title and priority are required'}), 400

    database = g.get('db_session')
    if database is None:
        return jsonify({'message': 'Database not available'}), 500

    result = UpdateTask(database, task_id, title, description, status, priority, due_date, user_id)

    if result:
        return jsonify({
            'message': 'Task updated successfully!',
            'task': result.to_dict()
        }), 200
    else:
        return jsonify({'message': 'Task update failed or task not found'}), 404



@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def deletetask(task_id):
    current_user = get_jwt_identity()
    user_id = current_user['id']

    # Check if user_id is valid
    if not user_id:
        return jsonify({"message": "Invalid or expired token"}), 401

    database = g.get('db_session')
    if database is None:
        return jsonify({'message': 'Database not available'}), 500

    result = DeleteTask(database, task_id, user_id)

    if result:
        return jsonify({
            'message': 'Task deleted successfully!'
        }), 200
    else:
        return jsonify({'message': 'Task deletion failed or task not found'}), 404


if __name__ == '__main__':
    session = InitializeDatabase()
    app.run()
