from internal.repository import User, Task
from sqlalchemy import func

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

    @staticmethod
    def fetch_user_tasks(database, user_id, status=None, priority=None, due_date=None, search_query=None):
        # Start the query to get tasks for the user
        query = database.query(Task).filter(Task.user_id == user_id)

        # Apply filtering based on provided query parameters
        if status:
            query = query.filter(Task.status == status)
        if priority:
            query = query.filter(Task.priority == priority)
        if due_date:
            query = query.filter(func.date(Task.due_date) == due_date)

        # Apply search functionality if search_query is provided
        if search_query:
            search_filter = (
                Task.title.ilike(f"%{search_query}%") | 
                Task.description.ilike(f"%{search_query}%")
            )
            query = query.filter(search_filter)

        try:
            # Execute the query and fetch tasks
            tasks = query.all()
            return tasks
        except Exception as e:
            print(f"Error fetching tasks: {e}")
            return None


    @staticmethod
    def update(database, task_id, title, description, status, priority, due_date, user_id):
        task = database.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

        if not task:
            return None

        # Update only the provided fields
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if priority is not None:
            task.priority = priority
        if due_date is not None:
            task.due_date = due_date  # Update due_date only if provided

        database.commit()
        return task

    @staticmethod
    def delete(database, task_id, user_id):
        task = database.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()

        if not task:
            return None

        database.delete(task)
        database.commit()
        return task
