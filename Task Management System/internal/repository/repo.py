from internal.repository import User, Task

def UserRegistrationRepo(database, username, password):
    # Check if the username already exists
    existing_user = database.query(User).filter_by(username=username).first()
    if existing_user:
        return False
    
    # If username does not exist, proceed with creating a new user
    new_user = User(username=username, password=password)
    database.add(new_user)
    database.commit()
    return True

def UserLoginRepo(database, username):
    user = database.query(User).filter_by(username=username).first()
    return user

class TaskRepository:
    @staticmethod
    def create(database, title, description, status, priority, due_date, user_id):
        new_task = Task(
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
            user_id=user_id
        )
        database.add(new_task)
        database.commit()
        return new_task
