import pytest
import requests
import json
from src import config

'''
            ========================================================
                            create_game tests
            ========================================================
'''

def test_input_error():
    resp = requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/create_game",
                         json={
                             'name': ""
                         })


    assert resp.status_code == 400

    resp = requests.post(config.url + "start/create_game",
                         json={
                             'name': "1234567831431431431423412341234123412341234234123412347951780954781780547890547890789027890789845547828790528209578095237890589038905378078493890328932790257839402357490327957324980257384952734590238475203947589234578349085732490572340527340527804873255555555555"
                         })

    assert resp.status_code == 400

def test_working_baic():
    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/create_game",
                         json={
                             'name': "123"
                         })

    assert resp.status_code == 200

    data = json.loads(resp.text)

    assert data['is_owner']
    assert data['num_cards'] == 6
    assert data['user_names'] == ['123']


'''
            ========================================================
                            join_game tests
            ========================================================
'''

def test_join_game_invalid_code():
    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/join_game",
                         json={
                             'game_id' : 1,
                             'name': "123"
                         })
    assert resp.status_code == 400

def test_join_game_invalid_name():
    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/create_game",
                         json={
                             'name': "123"
                         })

    assert resp.status_code == 200

    game_id = json.loads(resp.text)['game_id']

    resp = requests.post(config.url + "start/join_game",
                         json={
                             'game_id' : game_id,
                             'name': ""
                         })


    assert resp.status_code == 400

    resp = requests.post(config.url + "start/join_game",
                         json={
                             'game_id' : game_id,
                             'name': "123456783143143143142341234123412341234123423412341234795178095478178054789054789078902789078984554782879052820957809523789058903890537807849389032893279025783940235749032795732498025738495273459023847520394758923457834908573249057234052734052780487323123122312"
                         })

    assert resp.status_code == 400

    resp = requests.post(config.url + "start/join_game",
                         json={
                             'game_id' : game_id,
                             'name': "123"
                         })

    assert resp.status_code == 400

def test_join_game_many_players():
    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/create_game",
                         json={
                             'name': "123"
                         })

    game_id = json.loads(resp.text)['game_id']

    for i in range(7):
        
        print(game_id)
        
        resp = requests.post(config.url + "start/join_game",
                            json={
                                'game_id' : game_id,
                                'name': f"hello{i}"
                            })
        
        assert resp.status_code == 200
    

    resp = requests.post(config.url + "start/join_game",
                            json={
                                'game_id' : game_id,
                                'name': "hello"
                            })
        
    assert resp.status_code == 400
    

def test_join_game_working():
    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/create_game",
                         json={
                             'name': "123"
                         })

    game_id = json.loads(resp.text)['game_id']

    resp = requests.post(config.url + "start/join_game",
                         json={
                             'game_id' : game_id,
                             'name': "hello"
                         })
    data = json.loads((resp.text))

    assert data['num_cards'] == 6
    assert data['game_id'] == game_id

    # Check names in user_names
    assert len(data['user_names']) == 2
    assert "123" in data['user_names']
    assert "hello" in data['user_names']

'''
            ========================================================
                            change_num_cards tests
            ========================================================
'''

def test_change_num_cards_invalid_number():
    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/create_game",
                         json={
                             'name': "123"
                         })

    data = json.loads(resp.text)

    resp = requests.post(config.url + "start/change_num_cards", json = {'token' : data['token'], 'num_cards' : 52})
    assert resp.status_code == 400

    resp = requests.post(config.url + "start/join_game",
                            json={
                                'game_id' : data['game_id'],
                                'name': f"hello"
                            })
        
    assert resp.status_code == 200

    resp = requests.post(config.url + "start/change_num_cards", json = {'token' : data['token'], 'num_cards' : 26})
    assert resp.status_code == 400

def test_change_num_cards_invalid_token():
    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/change_num_cards", json = {'token' : 1, 'num_cards' : 52})
    assert resp.status_code == 403

def test_change_num_cards_not_owner():
    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/create_game",
                         json={
                             'name': "123"
                         })

    data = json.loads(resp.text)

    resp = requests.post(config.url + "start/join_game",
                            json={
                                'game_id' : data['game_id'],
                                'name': f"hello"
                            })
    
    assert resp.status_code == 200

    data = json.loads(resp.text)

    resp = requests.post(config.url + "start/change_num_cards", json = {'token' : data['token'], 'num_cards' : 10})
    assert resp.status_code == 403

def test_change_num_cards_working():
    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/create_game",
                         json={
                             'name': "123"
                         })
    
    data = json.loads(resp.text)

    resp = requests.post(config.url + "start/change_num_cards", json = {'token' : data['token'], 'num_cards' : 10})
    assert resp.status_code == 200

    resp = requests.post(config.url + "start/join_game",
                            json={
                                'game_id' : data['game_id'],
                                'name': f"hello"
                            })
        
    assert resp.status_code == 200

    data = json.loads(resp.text)

    assert data['num_cards'] == 10

'''
            ========================================================
                            update_start_screen tests
            ========================================================
'''

def test_invalid_token():
    requests.delete(config.url + "clear")

    resp = requests.get(config.url + "start/update_start_screen", params={'token' : 1})

    assert resp.status_code == 403
    
def test_working():

    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/create_game",
                         json={
                             'name': "123"
                         })

    data = json.loads(resp.text)

    resp = requests.get(config.url + "start/update_start_screen", params={'token' : data['token']})

    data_2 = json.loads(resp.text)

    assert data['num_cards'] == data_2['num_cards']
    assert data_2['is_owner'] == True

    resp = requests.post(config.url + "start/join_game",
                            json={
                                'game_id' : data['game_id'],
                                'name': f"hello"
                            })

    data_3 = json.loads(resp.text)

    resp = requests.get(config.url + "start/update_start_screen", params={'token' : data_3['token']})

    data_2 = json.loads(resp.text)

    assert data_2['is_owner'] == False

    assert "hello" in data_2['user_names']
    assert '123' in data_2['user_names']

    resp = requests.get(config.url + "start/update_start_screen", params={'token' : data['token']})

    data_2 = json.loads(resp.text)

    assert "hello" in data_2['user_names']
    assert '123' in data_2['user_names']

'''
            ========================================================
                            start_game tests
            ========================================================
'''

def test_start_game_invalid_token():
    requests.delete(config.url + "clear")

    resp = requests.post(config.url + "start/start_game", json={"token" : 1})

    assert resp.status_code == 403

def test_start_game_not_owner():
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

    resp = requests.post(config.url + "start/start_game", json={"token" : user_token})

    assert resp.status_code == 403

def test_start_game_working():
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

    resp = requests.post(config.url + "start/start_game", json={"token" : owner_token})

    data = json.loads(resp.text)
    
    assert data['game_started'] == True

    resp = requests.get(config.url + "start/update_start_screen", params={'token' : user_token})

    data = json.loads(resp.text)

    assert data['game_started'] == True