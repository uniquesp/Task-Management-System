import bcrypt
from ..repository.repo import UserRegistrationRepo, UserLoginRepo
import datetime
import jwt

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
        token = jwt.encode({
            'username': user.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
        }, 'SECRET_KEY', algorithm='HS256')
        
        return token
    else:
        return False

