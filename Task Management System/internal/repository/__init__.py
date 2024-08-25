from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum

# Define the SQLAlchemy base class
Base = declarative_base()

# Enum for task status
class TaskStatus(enum.Enum):
    TODO = "Todo"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


# Enum for task priority
class TaskPriority(enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

# Define the User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    # Relationship with tasks
    tasks = relationship('Task', back_populates='user')

# Define the Task model
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.TODO, nullable=False)
    # priority = Column(Integer, nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationship with user
    user = relationship('User', back_populates='tasks')

    def to_dict(self):
            return {
                'id': self.id,
                'title': self.title,
                'description': self.description,
                'status': self.status.value,  # Convert Enum to string
                'priority': self.priority,
                'due_date': self.due_date.isoformat() if self.due_date else None,
                'created_at': self.created_at.isoformat(),
                'updated_at': self.updated_at.isoformat(),
                'user_id': self.user_id,
            }
    

def InitializeDatabase():
    # Create an engine connected to tasks.db at the root directory
    engine = create_engine('sqlite:///tasks.db')
    
    # Bind the engine to a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create all tables
    Base.metadata.create_all(engine)
    print("Database initialized and tables created successfully.")
    return session
