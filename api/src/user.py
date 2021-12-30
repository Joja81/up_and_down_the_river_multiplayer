


from src.sql_classes.user_class import User


def create_user(name, session, play_order, is_owner = False):
    '''Creates user and returns their object, raises input error if name over 255 char or less then 1'''

    new_user = User(name = name, is_owner = is_owner, play_order = play_order)

    session.add(new_user)
    session.commit()

    return new_user