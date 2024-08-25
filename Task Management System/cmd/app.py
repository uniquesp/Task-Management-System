import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from internal.repository import InitializeDatabase
from internal.pkg.specs import ValidateRegistrationPayload
from internal.service.service import UserRegistration, UserLogin
from flask import Flask, request, jsonify, g

app = Flask(__name__)

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
def addtask():
    pass

@app.route('/api/tasks', methods=['GET'])
def gettask():
    pass


if __name__ == '__main__':
    session = InitializeDatabase()
    app.run()
