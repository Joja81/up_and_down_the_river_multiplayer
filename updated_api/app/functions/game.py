import random
import time

from app.models import Card, Game, Hand, Play, Round, Round_point, User, db

suits = ['C', 'D', 'H', 'S']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

END_ROUND_WAIT_TIME = 2 #Time until next round starts
END_GAME_WAIT_TIME = 100 # Time until game is wiped from db

def users_in_game(game):
    '''Returns a list of names of users in the game'''


    user_list = []

    for user in game.users:
        user_list.append(user.name)

    return user_list

def generate_round(game):
    '''Creates round and allocates cards, returns round'''

    cards = generate_card_list()

    trump_card = random.choice(cards)
    cards.remove(trump_card)

    curr_round = Round(round_num = game.round_num, card_num = game.card_num, trump_card_suit = trump_card['suit'], trump_card_rank = trump_card['rank'], game = game)


    for user in game.users:
        user_hand = Hand()

        for card in random.sample(cards, curr_round.card_num):
            curr_card = Card(suit = card['suit'], rank = card['rank'], round = curr_round)

            cards.remove(card)

            user_hand.cards.append(curr_card)

            db.session.add(curr_card)

        curr_round.hands.append(user_hand)
        user.hands.append(user_hand)
        
        db.session.add(user_hand)

    start_user_idx = game.round_num % len(game.users)

    start_user = User.query.filter(User.game == game, User.play_order == start_user_idx).first()
    curr_round.start_user = start_user
    
    db.session.add(curr_round)

    db.session.commit()

def prepare_new_round(game_id):
    game = Game.query.get(game_id)

    if game.round_num >= game.max_cards:
        game.card_num -= 1
    else:
        game.card_num += 1
    
    game.round_num += 1

    game.game_stage = "G"

    generate_round(game)

    db.session.commit()


def generate_card_list():
    '''Returns list of cards'''

    cards = []

    for suit in suits:
        for rank in ranks:
            cards.append({'suit' : suit, 'rank' : rank})

    return cards

def start_play(game, curr_round):
    
    new_play = Play(play_num = 1, current_user = curr_round.start_user, round = curr_round, game = game)

    db.session.add(new_play)
    db.session.commit()

def next_play(game_id, round_id):

    game = Game.query.get(game_id)

    curr_round = Round.query.get(round_id)

    play = Play.query.filter(Play.round == curr_round).order_by(Play.play_num.desc()).first()

    start_player = play.winner

    new_play = Play(play_num = len(curr_round.plays) + 1, current_user = start_player, round = curr_round, game = game)

    db.session.add(new_play)
    db.session.commit()

def end_round(curr_round, game):
    calculate_score(curr_round)

    if game.round_num == (game.max_cards * 2 - 1):
        game.game_stage = "F"
        # TODO implement system that clears game after set amount of time
        # clear_game(game.id)
    else:
        game.game_stage = "R"
        game.new_round_time = time.time() + END_ROUND_WAIT_TIME
       
    db.session.commit()


def calculate_score(curr_round):

    for guess in curr_round.guesses:
        num_wins = Play.query.filter(Play.round == curr_round, Play.winner == guess.user).count()

        if num_wins == guess.guess:
            score = 10 + num_wins * 5
        else:
            score = 0
        
        user_points = Round_point(points = score, user = guess.user, round = curr_round)

        db.session.add(user_points)
    
    db.session.commit()

def clear_game(game_id):
    pass
    #TODO clear game from db