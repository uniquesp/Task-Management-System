from internal.repository import User

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
