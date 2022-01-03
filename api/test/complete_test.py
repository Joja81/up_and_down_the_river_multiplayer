import time
import json
import requests

from src import config


def test_2_card_test():

    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/create_game",
                         json={
                             'name': "user_1"
                         })
    
    data = json.loads(resp.text)
    
    game_id = data['game_id']
    owner_token = data['token']

    resp = requests.post(config.url + "start/change_num_cards", json = {'token' : data['token'], 'num_cards' : 2})
    assert resp.status_code == 200

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

    resp = requests.get(config.url + "play/get_curr_cards", params= {'token' : owner_token})
    cards_1 = json.loads(resp.text)['cards'][0]

    resp = requests.get(config.url + "play/get_curr_cards", params= {'token' : user_token})
    cards_2 = json.loads(resp.text)['cards'][0]

    resp = requests.post(config.url + "play/give_play", json = {'token' : user_token, 'play' : cards_2})

    assert resp.status_code == 200

    resp = requests.post(config.url + "play/give_play", json = {'token' : owner_token, 'play' : cards_1})

    assert resp.status_code == 200

    time.sleep(5)

    resp = requests.get(config.url + "guess/collect_cards",
                         params={
                             'token': owner_token
                         })
    
    cards_1 = json.loads(resp.text)['cards']

    assert len(cards_1) == 2

    resp = requests.get(config.url + "guess/collect_cards",
                         params={
                             'token': user_token
                         })
    
    cards_2 = json.loads(resp.text)['cards']

    assert len(cards_2) == 2

    resp = requests.get(config.url + "guess/get_guesses", params={'token' : owner_token})

    data = json.loads(resp.text)

    assert data['user_guess']

    resp = requests.post(config.url + "guess/give_guess", json = {'token' : owner_token, 'guess' : 1})

    assert resp.status_code == 200

    resp = requests.get(config.url + "guess/get_guesses", params={'token' : user_token})

    data = json.loads(resp.text)

    assert data['user_guess']

    resp = requests.post(config.url + "guess/give_guess", json = {'token' : user_token, 'guess' : 1})

    assert resp.status_code == 400

    resp = requests.post(config.url + "guess/give_guess", json = {'token' : user_token, 'guess' : 0})

    assert resp.status_code == 200

    resp = requests.get(config.url + "guess/get_guesses", params={'token' : user_token})

    data = json.loads(resp.text)

    assert len(data['guesses']) == 2

    assert data['is_guessing_complete']

    resp = requests.get(config.url + "play/get_current_play", params= {'token' : owner_token})

    data = json.loads(resp.text)

    assert data['cards'] == []
    assert data['play_num'] == 1
    assert data['is_player_turn'] == True
    assert data['is_finished'] == False

    resp = requests.post(config.url + "play/give_play", json = {'token' : owner_token, 'play' : cards_1[0]})

    if resp.status_code != 200:
        resp = requests.post(config.url + "play/give_play", json = {'token' : owner_token, 'play' : cards_1[1]})
        assert resp.status_code == 200

    resp = requests.get(config.url + "play/get_current_play", params= {'token' : user_token})

    data = json.loads(resp.text)

    assert data['cards'] == [cards_1[0]] or data['cards'] == [cards_1[1]]
    assert data['play_num'] == 1
    assert data['is_player_turn'] == True
    assert data['is_finished'] == False

    resp = requests.post(config.url + "play/give_play", json = {'token' : user_token, 'play' : cards_2[0]})

    if resp.status_code != 200:
        resp = requests.post(config.url + "play/give_play", json = {'token' : user_token, 'play' : cards_2[1]})
        assert resp.status_code == 200
    
    resp = requests.get(config.url + "play/get_current_play", params= {'token' : user_token})
    data = json.loads(resp.text)

    assert data['is_finished'] == True
    assert data['is_player_turn'] == False

    resp = requests.get(config.url + "play/get_curr_wins", params= {'token' : owner_token})
    scores = json.loads(resp.text)['scores']

    user_1_loss = {'name' : 'user_1', 'score' : 0}
    user_1_win = {'name' : 'user_1', 'score' : 1}

    user_2_loss = {'name' : 'user_2', 'score' : 0}
    user_2_win = {'name' : 'user_2', 'score' : 1}

    assert (user_1_win in scores and user_2_loss in scores) or (user_1_loss in scores and user_2_win in scores)

    time.sleep(5)

    resp = requests.get(config.url + "play/get_current_play", params= {'token' : user_token})
    data = json.loads(resp.text)

    assert data['play_num'] == 2

    if data['is_player_turn']:
        resp = requests.post(config.url + "play/give_play", json = {'token' : user_token, 'play' : cards_2[0]})

        if resp.status_code != 200:
            resp = requests.post(config.url + "play/give_play", json = {'token' : user_token, 'play' : cards_2[1]})
            assert resp.status_code == 200
        
        resp = requests.post(config.url + "play/give_play", json = {'token' : owner_token, 'play' : cards_1[0]})

        if resp.status_code != 200:
            resp = requests.post(config.url + "play/give_play", json = {'token' : owner_token, 'play' : cards_1[1]})
            assert resp.status_code == 200
    else:
        resp = requests.post(config.url + "play/give_play", json = {'token' : owner_token, 'play' : cards_1[0]})

        if resp.status_code != 200:
            resp = requests.post(config.url + "play/give_play", json = {'token' : owner_token, 'play' : cards_1[1]})
            assert resp.status_code == 200
        
        resp = requests.post(config.url + "play/give_play", json = {'token' : user_token, 'play' : cards_2[0]})

        if resp.status_code != 200:
            resp = requests.post(config.url + "play/give_play", json = {'token' : user_token, 'play' : cards_2[1]})
            assert resp.status_code == 200

    resp = requests.get(config.url + "result/get_curr_results", params={'token' : user_token})

    assert resp.status_code == 200

    time.sleep(5)

    resp = requests.get(config.url + "result/get_curr_results", params={'token' : user_token})
    data = json.loads(resp.text)
    assert data['guessing_started']

    resp = requests.post(config.url + "guess/give_guess", json = {'token' : user_token, 'guess' : 1})

    assert resp.status_code == 200

    resp = requests.post(config.url + "guess/give_guess", json = {'token' : owner_token, 'guess' : 1})

    assert resp.status_code == 200
    
    resp = requests.get(config.url + "play/get_curr_cards", params= {'token' : owner_token})
    
    assert len(json.loads(resp.text)['cards']) == 1

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

    resp = requests.get(config.url + "result/get_curr_results", params={'token' : user_token})
    data = json.loads(resp.text)
    assert data['game_finished']