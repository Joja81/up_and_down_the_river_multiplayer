import jwt
from app.functions.error import AccessError

from app.models import User_session, db



SECRET = "changeTHIS"

def generate_token(user):
    '''Creates token for user given user object'''

    user_session = User_session(user = user)

    db.session.add(user_session)
    db.session.commit()

    token = jwt.encode({'auth_user_id': user.id,
                       'session_id': user_session.id}, SECRET, algorithm='HS256')

    return token

def token_check(token):
    '''Checks validity of token and returns id if valid, raisies Access error if token invalid'''


    try:
        data = jwt.decode(token, SECRET, algorithms=['HS256'])
    except BaseException as all_errors:
        raise AccessError(description= "Token is not valid") from all_errors

    session_data = User_session.query.get(data['session_id'])

    if session_data == None or session_data.user_id != data['auth_user_id'] :
        raise AccessError(description= "Token is not valid")
    
    return session_data.user_id
