
import json
import requests
from requests.api import request

import config
'''
            ========================================================
                            get_curr_cards tests
            ========================================================
'''


def test_get_curr_card_invalid_token():
    requests.delete(config.url + "clear")

    resp = requests.get(config.url + "play/get_curr_cards", params= {'token' : 1})

    assert resp.status_code == 403

def test_get_curr_card_not_playing():
    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/create_game",
                         json={
                             'name': "123"
                         })
    
    data = json.loads(resp.text)
    
    game_id = data['game_id']
    owner_token = data['token']

    resp = requests.post(config.url + "start/join_game",
                         json={
                             'game_id' : game_id,
                             'name': "hello"
                         })
    data = json.loads(resp.text)

    user_token = data['token']

    resp = requests.get(config.url + "play/get_curr_cards", params= {'token' : owner_token})

    assert resp.status_code == 400

    resp = requests.get(config.url + "play/get_curr_cards", params= {'token' : user_token})

    assert resp.status_code == 400

    requests.post(config.url + "start/start_game", json={"token" : owner_token})

    resp = requests.get(config.url + "play/get_curr_cards", params= {'token' : owner_token})

    assert resp.status_code == 400

    resp = requests.get(config.url + "play/get_curr_cards", params= {'token' : user_token})

    assert resp.status_code == 400

def test_get_curr_card_working():
    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/create_game",
                         json={
                             'name': "user_1"
                         })
    
    data = json.loads(resp.text)
    
    game_id = data['game_id']
    owner_token = data['token']

    resp = requests.post(config.url + "start/join_game",
                         json={
                             'game_id' : game_id,
                             'name': "user_2"
                         })
    data = json.loads(resp.text)

    user_token = data['token']

    requests.post(config.url + "start/start_game", json={"token" : owner_token})

    resp = requests.get(config.url + "guess/collect_cards",
                         params={
                             'token': owner_token
                         })
    
    cards_1_guess = json.loads(resp.text)

    resp = requests.get(config.url + "guess/collect_cards",
                         params={
                             'token': user_token
                         })
    
    cards_2_guess = json.loads(resp.text)


    resp = requests.post(config.url + "guess/give_guess", json = {'token' : user_token, 'guess' : 1})

    resp = requests.post(config.url + "guess/give_guess", json = {'token' : owner_token, 'guess' : 1})

    resp = requests.get(config.url + "play/get_curr_cards", params= {'token' : owner_token})

    assert json.loads(resp.text) == cards_1_guess

    resp = requests.get(config.url + "play/get_curr_cards", params= {'token' : user_token})

    assert json.loads(resp.text) == cards_2_guess

'''
            ========================================================
                            get_current_play tests
            ========================================================
'''


def test_get_current_play_invalid_token():

    requests.delete(config.url + "clear")

    resp = requests.get(config.url + "play/get_current_play", params= {'token' : 1})

    assert resp.status_code == 403

def test_get_current_play_not_play_stage():
    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/create_game",
                         json={
                             'name': "123"
                         })
    
    data = json.loads(resp.text)
    
    game_id = data['game_id']
    owner_token = data['token']

    resp = requests.post(config.url + "start/join_game",
                         json={
                             'game_id' : game_id,
                             'name': "hello"
                         })
    data = json.loads(resp.text)

    user_token = data['token']

    resp = requests.get(config.url + "play/get_current_play", params= {'token' : owner_token})

    assert resp.status_code == 400

    resp = requests.get(config.url + "play/get_current_play", params= {'token' : user_token})

    assert resp.status_code == 400

    requests.post(config.url + "start/start_game", json={"token" : owner_token})

    resp = requests.get(config.url + "play/get_current_play", params= {'token' : owner_token})

    assert resp.status_code == 400

    resp = requests.get(config.url + "play/get_current_play", params= {'token' : user_token})

    assert resp.status_code == 400


def test_get_current_play_working():
    owner_token, user_token = setup_game()

    resp = requests.get(config.url + "play/get_current_play", params= {'token' : owner_token})

    data = json.loads(resp.text)

    assert len(data['cards']) == 0
    assert data['play_num'] == 1
    assert data['curr_user_turn'] == "user_2"
    assert data['is_player_turn'] == False
    assert data['is_finished'] == False

    resp = requests.get(config.url + "play/get_current_play", params= {'token' : user_token})

    data = json.loads(resp.text)

    assert len(data['cards']) == 0
    assert data['play_num'] == 1
    assert data['curr_user_turn'] == "user_2"
    assert data['is_player_turn'] == True
    assert data['is_finished'] == False

'''
            ========================================================
                            get_currr_wins tests
            ========================================================
'''

def test_get_curr_wins_invalid_token():

    requests.delete(config.url + "clear")

    resp = requests.get(config.url + "play/get_curr_wins", params= {'token' : 1})

    assert resp.status_code == 403

def test_get_curr_wins_invalid_stage():
    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/create_game",
                         json={
                             'name': "123"
                         })
    
    data = json.loads(resp.text)
    
    game_id = data['game_id']
    owner_token = data['token']

    resp = requests.post(config.url + "start/join_game",
                         json={
                             'game_id' : game_id,
                             'name': "hello"
                         })
    data = json.loads(resp.text)

    user_token = data['token']

    resp = requests.get(config.url + "play/get_curr_wins", params= {'token' : owner_token})

    assert resp.status_code == 400

    resp = requests.get(config.url + "play/get_curr_wins", params= {'token' : user_token})

    assert resp.status_code == 400

    requests.post(config.url + "start/start_game", json={"token" : owner_token})

    resp = requests.get(config.url + "play/get_curr_wins", params= {'token' : owner_token})

    assert resp.status_code == 400

    resp = requests.get(config.url + "play/get_curr_wins", params= {'token' : user_token})

    assert resp.status_code == 400

def test_get_curr_wins_working():
    owner_token, user_token = setup_game()

    resp = requests.get(config.url + "play/get_curr_wins", params= {'token' : owner_token})
    
    scores = json.loads(resp.text)['scores']

    assert len(scores) == 2

    assert {'name' : 'user_1', 'score' : 0} in scores
    assert {'name' : 'user_2', 'score' : 0} in scores

    resp = requests.get(config.url + "play/get_curr_wins", params= {'token' : user_token})
    
    scores = json.loads(resp.text)['scores']

    assert len(scores) == 2

    assert {'name' : 'user_1', 'score' : 0} in scores
    assert {'name' : 'user_2', 'score' : 0} in scores

'''
            ========================================================
                            give_play tests
            ========================================================
'''

def test_give_play_invalid_token():
    requests.delete(config.url + "clear")

    card = {'suit' : 'C', 'rank' : '2'}

    resp = requests.post(config.url + "play/give_play", json= {'token' : 1, 'play' : card})

    assert resp.status_code == 403

def test_give_play_invalid_stage():
    card = {'suit' : 'C', 'rank' : '2'}

    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/create_game",
                         json={
                             'name': "123"
                         })
    
    data = json.loads(resp.text)
    
    game_id = data['game_id']
    owner_token = data['token']

    resp = requests.post(config.url + "start/join_game",
                         json={
                             'game_id' : game_id,
                             'name': "hello"
                         })
    data = json.loads(resp.text)

    user_token = data['token']

    resp = requests.post(config.url + "play/give_play", json= {'token' : owner_token, 'play' : card})

    assert resp.status_code == 400

    resp = requests.post(config.url + "play/give_play", json= {'token' : user_token, 'play' : card})

    assert resp.status_code == 400

    requests.post(config.url + "start/start_game", json={"token" : owner_token})

    resp = requests.post(config.url + "play/give_play", json= {'token' : owner_token, 'play' : card})

    assert resp.status_code == 400

    resp = requests.post(config.url + "play/give_play", json= {'token' : user_token, 'play' : card})

    assert resp.status_code == 400

def test_give_card_working():
    owner_token, user_token = setup_game()
    
    resp = requests.get(config.url + "play/get_curr_cards", params= {'token' : owner_token})
    cards_1 = json.loads(resp.text)['cards'][0]

    resp = requests.get(config.url + "play/get_curr_cards", params= {'token' : user_token})
    cards_2 = json.loads(resp.text)['cards'][0]

    resp = requests.post(config.url + "play/give_play", json = {'token' : user_token, 'play' : cards_2})

    assert resp.status_code == 200

    
    resp = requests.get(config.url + "play/get_curr_cards", params= {'token' : user_token})
    assert len(json.loads(resp.text)['cards']) == 0

    resp = requests.get(config.url + "play/get_current_play", params= {'token' : owner_token})

    data = json.loads(resp.text)

    assert data['cards'] == [cards_2]
    assert data['play_num'] == 1
    assert data['curr_user_turn'] == "user_1"
    assert data['is_player_turn'] == True
    assert data['is_finished'] == False

    resp = requests.get(config.url + "play/get_current_play", params= {'token' : user_token})

    data = json.loads(resp.text)

    assert data['cards'] == [cards_2]
    assert data['play_num'] == 1
    assert data['curr_user_turn'] == "user_1"
    assert data['is_player_turn'] == False
    assert data['is_finished'] == False

    resp = requests.post(config.url + "play/give_play", json = {'token' : owner_token, 'play' : cards_2})

    assert resp.status_code == 400

    resp = requests.post(config.url + "play/give_play", json = {'token' : owner_token, 'play' : cards_1})

    assert resp.status_code == 200

    resp = requests.get(config.url + "play/get_current_play", params= {'token' : owner_token})

    data = json.loads(resp.text)

    assert data['cards'] == [cards_2, cards_1]
    assert data['play_num'] == 1
    assert data['is_player_turn'] == False
    assert data['is_finished'] == True

    resp = requests.get(config.url + "play/get_current_play", params= {'token' : user_token})

    data = json.loads(resp.text)

    assert data['cards'] == [cards_2, cards_1]
    assert data['play_num'] == 1
    assert data['is_player_turn'] == False
    assert data['is_finished'] == True


'''
Extra stuff
'''

def setup_game():
    '''sets up base game for testing'''

    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/create_game",
                         json={
                             'name': "user_1"
                         })
    
    data = json.loads(resp.text)
    
    game_id = data['game_id']
    owner_token = data['token']

    resp = requests.post(config.url + "start/join_game",
                         json={
                             'game_id' : game_id,
                             'name': "user_2"
                         })
    data = json.loads(resp.text)

    user_token = data['token']

    requests.post(config.url + "start/start_game", json={"token" : owner_token})

    resp = requests.post(config.url + "guess/give_guess", json = {'token' : user_token, 'guess' : 1})

    assert resp.status_code == 200

    resp = requests.post(config.url + "guess/give_guess", json = {'token' : owner_token, 'guess' : 1})

    return owner_token, user_token