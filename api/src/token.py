from src.error import AccessError
from src.sql_classes.user_session import User_session
import jwt

SECRET = "changeTHIS"

def generate_token(user, session):
    '''Creates token for user given user object'''

    user_session = User_session(user = user)

    session.add(user_session)
    session.commit()

    token = jwt.encode({'auth_user_id': user.id,
                       'session_id': user_session.id}, SECRET, algorithm='HS256')

    return token

def token_check(token, session):
    '''Checks validity of token and returns id if valid, raisies Access error if token invalid'''


    try:
        data = jwt.decode(token, SECRET, algorithms=['HS256'])
    except BaseException as all_errors:
        raise AccessError(description= "Token is not valid") from all_errors


    session_data = session.query(User_session).get(data['session_id'])

    if session_data == None or session_data.user_id != data['auth_user_id'] :
        raise AccessError(description= "Token is not valid")
    
    return session_data.user_id
