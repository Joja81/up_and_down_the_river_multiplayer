import json
import requests

import config

'''
            ========================================================
                            collect_cards tests
            ========================================================
'''

def test_collect_cards_invalid_token():
    requests.delete(config.url + "clear")

    resp = requests.get(config.url + "guess/collect_cards",
                         params={
                             'token': "1"
                         })
    
    assert resp.status_code == 403

def test_collect_cards_game_not_started():
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
    data = json.loads((resp.text))

    user_token = data['token']

    resp = requests.get(config.url + "guess/collect_cards",
                         params={
                             'token': owner_token
                         })
    
    assert resp.status_code == 400

    resp = requests.get(config.url + "guess/collect_cards",
                         params={
                             'token': user_token
                         })
    
    assert resp.status_code == 400


def test_collect_cards_working():
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

    requests.post(config.url + "start/start_game", json={"token" : owner_token})

    resp = requests.get(config.url + "guess/collect_cards",
                         params={
                             'token': owner_token
                         })
    
    cards_1 = json.loads(resp.text)['cards']

    assert len(cards_1) == 1
    cards_1 = cards_1[0]

    suits = ["C", "D", "H", "S"]
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    

    assert cards_1['suit'] in suits
    assert cards_1['rank'] in ranks

    resp = requests.get(config.url + "guess/collect_cards",
                         params={
                             'token': user_token
                         })
    
    cards_2 = json.loads(resp.text)['cards']

    assert len(cards_2) == 1
    cards_2 = cards_2[0]

    assert cards_2['suit'] in ['C', 'D', 'H', 'S']
    assert cards_2['rank'] in ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    assert cards_1 != cards_2

'''
            ========================================================
                            get_guesses tests
            ========================================================
'''

def test_get_guesses_invalid_token():
    requests.delete(config.url + "clear")

    resp = requests.get(config.url + "guess/get_guesses", params={'token' : 1})
    
    assert resp.status_code == 403

def test_get_guesses_not_guessing():
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

    resp = requests.get(config.url + "guess/get_guesses", params={'token' : owner_token})
    
    assert resp.status_code == 400

    resp = requests.get(config.url + "guess/get_guesses", params={'token' : user_token})
    
    assert resp.status_code == 400

def test_get_guesses_working():

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

    resp = requests.get(config.url + "guess/get_guesses", params={'token' : owner_token})

    data = json.loads(resp.text)

    assert len(data['guesses']) == 0
    assert data['current_guesser'] == 'user_2'
    assert data['user_guess'] == False
    assert data['is_guessing_complete'] == False

    resp = requests.get(config.url + "guess/get_guesses", params={'token' : user_token})

    data = json.loads(resp.text)

    assert len(data['guesses']) == 0
    assert data['current_guesser'] == 'user_2'
    assert data['user_guess'] == True
    assert data['is_guessing_complete'] == False

'''
            ========================================================
                            give_guess tests
            ========================================================
'''


def test_give_guess_invalid_token():
    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "guess/give_guess", json = {'token' : 1, 'guess' : 1})

    assert resp.status_code == 403

def test_give_guess_not_guess():
    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/create_game",
                         json={
                             'name': "user_1"
                         })
    
    data = json.loads(resp.text)
    owner_token = data['token']

    resp = requests.post(config.url + "guess/give_guess", json = {'token' : owner_token, 'guess' : 1})

    assert resp.status_code == 400

def test_give_guess_not_user_turn():
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

    resp = requests.post(config.url + "guess/give_guess", json = {'token' : owner_token, 'guess' : 1})

    assert resp.status_code == 400

def test_give_guess_working():
    #Also tests get_guesses

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

    # Test get_guesses

    resp = requests.get(config.url + "guess/get_guesses", params={'token' : user_token})

    data = json.loads(resp.text)

    assert data['guesses'] == [{'player_name' : 'user_2', 'player_guess' : 1}]
    assert data['current_guesser'] == 'user_1'
    assert data['user_guess'] == False
    assert data['is_guessing_complete'] == False

    # Check that won't let reenter bid
    
    resp = requests.post(config.url + "guess/give_guess", json = {'token' : user_token, 'guess' : 1})

    assert resp.status_code == 400

    # Test that won't let user enter invalid guess

    resp = requests.post(config.url + "guess/give_guess", json = {'token' : owner_token, 'guess' : 0})

    assert resp.status_code == 400

    resp = requests.post(config.url + "guess/give_guess", json = {'token' : owner_token, 'guess' : -1})

    assert resp.status_code == 400

    resp = requests.post(config.url + "guess/give_guess", json = {'token' : owner_token, 'guess' : 2})

    assert resp.status_code == 400

    # Enter proper result

    resp = requests.post(config.url + "guess/give_guess", json = {'token' : owner_token, 'guess' : 1})

    assert resp.status_code == 200

    resp = requests.get(config.url + "guess/get_guesses", params={'token' : owner_token})

    data = json.loads(resp.text)

    assert len(data['guesses']) == 2
    assert {'player_name' : 'user_1', 'player_guess' : 1} in data['guesses']
    assert {'player_name' : 'user_2', 'player_guess' : 1} in data['guesses']
    assert data['user_guess'] == False
    assert data['is_guessing_complete'] == True