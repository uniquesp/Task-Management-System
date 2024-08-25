import bcrypt
from ..repository.repo import TaskRepository, UserRegistrationRepo, UserLoginRepo
from datetime import datetime
from flask_jwt_extended import create_access_token


def UserRegistration(database, username, password):
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

  result = UserRegistrationRepo(database, username, hashed_password)
  if result == True:
    return True
  else:
    return False

def UserLogin(database, username, password):
    user = UserLoginRepo(database, username)
    
    if user is None:
        return False

    if bcrypt.checkpw(password.encode('utf-8'), user.password):
        # Create JWT access token with user ID as part of the identity
        token = create_access_token(identity={'id': user.id})
        return token
    else:
        return False
    
    
def CreateTask(database, title, description, status, priority, due_date, user_id):
    if due_date:
        due_date = datetime.strptime(due_date, '%Y-%m-%d')

    task = TaskRepository.create(database, title, description, status, priority, due_date, user_id)
    return task


def FetchUserTasks(database, user_id, status=None, priority=None, due_date=None, search_query=None):
    tasks = TaskRepository.fetch_user_tasks(database, user_id, status, priority, due_date, search_query)
    return tasks


def UpdateTask(database, task_id, title, description, status, priority, due_date, user_id):
    if due_date:
        due_date = datetime.strptime(due_date, '%Y-%m-%d')

    task = TaskRepository.update(database, task_id, title, description, status, priority, due_date, user_id)
    return task
