import time

from requests.sessions import session
from src.error import AccessError, InputError
from src.game import generate_round, users_in_game
from src.sql_classes.game_class import Game
from src.sql_classes.user_class import User
from src.token import generate_token
from src.user import create_user


def create_new_game(name, session):
    '''Creates a new game with new user as owner'''

    DEFAULT_CARD_NUMBER = 6
    
    #Create user

    check_name(name, None, session)

    user = create_user(name, session, 0,is_owner= True)

    # Create new game

    new_game = Game(time_start = time.time(), max_cards = DEFAULT_CARD_NUMBER, game_stage = "S", card_num = 1, round_num = 1)

    user.game = new_game

    session.add(new_game)
    session.commit()

    token = generate_token(user, session)

    return {
        'token' : token,
        'num_cards' : new_game.max_cards,
        'is_owner' : user.is_owner,
        'game_id' : new_game.id,
        'user_names' : users_in_game(new_game, session)
    }

def join_game(name, game_code, session):

    game = session.query(Game).get(game_code)

    if game is None:
        raise InputError(description = "Game code is invalid")
    
    check_name(name, game, session)

    # Check that correct num of cards left

    if (len(game.users) + 1)* game.max_cards + 1 > 52:
        raise InputError(description = "Too many users in the game for number of cards")

    user = create_user(name, session, len(game.users))

    user.game = game

    session.add(user)
    session.commit()

    token = generate_token(user, session)
    (token)

    return {
        'token' : token, 
        'num_cards' : game.max_cards,
        'is_owner' : user.is_owner,
        'game_id' : game.id,
        'user_names' : users_in_game(game, session)
    }

def change_num_cards(auth_user_id, num_cards, session):
    user = session.query(User).get(auth_user_id)

    if not user.is_owner:
        raise AccessError(description = "User is not the owner of this game")
    
    if num_cards < 1:
        raise InputError(description = "Cannot have less then 1 card")
    
    game = user.game

    if (len(game.users))* num_cards + 1 > 52:
        raise InputError(description = "Too many users in the game for number of cards")

    game.max_cards = num_cards
    session.commit()

def update_start_screen(auth_user_id, session):
    user = session.query(User).get(auth_user_id)

    game = user.game

    return {
        'num_cards' : game.max_cards,
        'is_owner' : user.is_owner,
        'game_id' : game.id,
        'user_names' : users_in_game(game, session),
        'game_started' : game.game_stage != "S"
    }

def start_game(auth_user_id, session):
    user = session.query(User).get(auth_user_id)

    if not user.is_owner:
        raise AccessError(description="User is not the owner of this game")

    game = user.game

    game.game_stage = "G"

    generate_round(game, session)

    session.commit()

    return {'game_started' : True}


def check_name(name, game, session):
    '''Checks for valid name in given game, if game is not created game is given as None'''

    if len(name) < 1 or len(name) > 255:
        raise InputError(description = "Name too short or too long")
    
    if game != None:
        if name in users_in_game(game, session):
            raise InputError(description = "Name is already being used")