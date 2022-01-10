from datetime import datetime
import json
from re import S
import sys
import signal
from json import dumps, loads
from flask import Flask, request
from flask_cors import CORS
from sqlalchemy import engine
from sqlalchemy.orm.session import Session

from src import config
from src.guess import collect_cards, get_guesses, give_guess
from src.play import get_curr_cards, get_curr_wins, get_current_play, give_play
from src.result import get_curr_results
from src.sql_functions.base import Base
from src.sql_functions.sql_generate import generate_engine
from src.start import change_num_cards, create_new_game, join_game, start_game, update_start_screen
from src.token import token_check

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)


def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response


APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

engine = None
session = None

# Setting up connection to db
@APP.before_first_request
def setup_db_engine():
    global engine
    engine = generate_engine()

@APP.before_request
def setup_db_session():
    global session
    session = Session(engine)

@APP.after_request
def close_db_session(response):
    session.close()
    return response

# Clear route

@APP.route("/clear", methods = ["DELETE"])
def clear_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return {}

# Start routes
@APP.route("/start/create_game", methods = ["POST"])
def start_create_game():
    data = request.get_json()

    return json.dumps(create_new_game(data['name'], session))

@APP.route("/start/join_game", methods = ["POST"])
def start_join_game():
    data = request.get_json()

    print(data)

    return json.dumps(join_game(data['name'], data['game_id'], session))

@APP.route("/start/change_num_cards", methods = ["POST"])
def start_change_num_cards():
    data = request.get_json()

    auth_user_id = token_check(data['token'], session)

    change_num_cards(auth_user_id, data['num_cards'], session)

    return {}

@APP.route("/start/update_start_screen", methods = ["GET"])
def start_update_start_screen():

    token = request.args.get('token')

    auth_user_id = token_check(token, session)

    return json.dumps(update_start_screen(auth_user_id, session))

@APP.route("/start/start_game", methods = ["POST"])
def start_start_game():
    data = request.get_json()

    auth_user_id = token_check(data['token'], session)

    return json.dumps(start_game(auth_user_id, session))

# Guess routes
@APP.route("/guess/collect_cards", methods = ['GET'])
def guess_collect_cards():
    token = request.args.get('token')

    auth_user_id = token_check(token, session)

    return json.dumps(collect_cards(auth_user_id, session))

@APP.route("/guess/get_guesses", methods = ['GET'])
def guess_get_guesses():
    token = request.args.get('token')

    auth_user_id = token_check(token, session)

    return json.dumps(get_guesses(auth_user_id, session))

@APP.route("/guess/give_guess", methods = ["POST"])
def guess_give_guess():
    data = request.get_json()

    auth_user_id = token_check(data['token'], session)

    return json.dumps(give_guess(auth_user_id, data['guess'], session))

# Play routes
@APP.route("/play/get_curr_cards", methods = ['GET'])
def play_get_curr_cards():
    token = request.args.get('token')

    auth_user_id = token_check(token, session)

    return json.dumps(get_curr_cards(auth_user_id, session))

@APP.route("/play/get_current_play", methods = ['GET'])
def play_get_current_play():
    token = request.args.get('token')

    auth_user_id = token_check(token, session)

    return json.dumps(get_current_play(auth_user_id, session))

@APP.route("/play/get_curr_wins", methods = ['GET'])
def play_get_curr_wins():
    token = request.args.get('token')

    auth_user_id = token_check(token, session)

    return json.dumps(get_curr_wins(auth_user_id, session))

@APP.route("/play/give_play", methods = ["POST"])
def play_give_play():
    data = request.get_json()

    auth_user_id = token_check(data['token'], session)

    return json.dumps(give_play(auth_user_id, data['play'], session, engine))

# Results routs
@APP.route("/result/get_curr_results", methods = ['GET'])
def result_get_curr_results():
    token = request.args.get('token')

    auth_user_id = token_check(token, session)

    return json.dumps(get_curr_results(auth_user_id, session))


if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully)  # For coverage
    APP.run(port=config.port, debug=True)  # Do not edit this port
    engine
