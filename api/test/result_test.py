import json
import requests

from src import config
from test.play_test import setup_game

'''
            ========================================================
                            get_curr_results tests
            ========================================================
'''

def test_get_curr_results_invalid_token():
    requests.delete(config.url + "clear")

    resp = requests.get(config.url + "result/get_curr_results", params={'token' : 1})

    assert resp.status_code == 403

def test_get_curr_results_working():

    owner_token, user_token = setup_game()
    
    resp = requests.get(config.url + "play/get_curr_cards", params= {'token' : owner_token})
    cards_1 = json.loads(resp.text)['cards'][0]

    resp = requests.get(config.url + "play/get_curr_cards", params= {'token' : user_token})
    cards_2 = json.loads(resp.text)['cards'][0]

    resp = requests.post(config.url + "play/give_play", json = {'token' : user_token, 'play' : cards_2})

    assert resp.status_code == 200

    resp = requests.post(config.url + "play/give_play", json = {'token' : owner_token, 'play' : cards_1})

    assert resp.status_code == 200

    resp = requests.get(config.url + "result/get_curr_results", params={'token' : user_token})

    data = json.loads(resp.text)

    assert not data['game_finished']

    results = data['results']

    user_1_win = {'name' : 'user_1', 'score' : 15, 'change' : 15, 'is_user' : False}
    user_2_win = {'name' : 'user_2', 'score' : 15, 'change' : 15, 'is_user' : True}

    user_1_lose = {'name' : 'user_1', 'score' : 0, 'change' : 0, 'is_user' : False}
    user_2_lose = {'name' : 'user_2', 'score' : 0, 'change' : 0, 'is_user' : True}

    assert user_1_win in results or user_2_win in results
    assert not(user_1_win in results and user_2_win in results)

    assert user_1_lose in results or user_2_lose in results