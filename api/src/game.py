import random
import threading

from sqlalchemy.orm.session import Session
from src.sql_classes.card_class import Card
from src.sql_classes.game_class import Game
from src.sql_classes.hand_class import Hand
from src.sql_classes.play_class import Play
from src.sql_classes.round_class import Round
from src.sql_classes.round_points_class import Round_point
from src.sql_classes.user_class import User

suits = ['C', 'D', 'H', 'S']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

END_ROUND_WAIT_TIME = 2 #Time until next round starts

def users_in_game(game, session):
    '''Returns a list of names of users in the game'''


    user_list = []

    for user in game.users:
        user_list.append(user.name)

    return user_list

def generate_round(game, session):
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

            session.add(curr_card)

        curr_round.hands.append(user_hand)
        user.hands.append(user_hand)
        
        session.add(user_hand)

    start_user_idx = game.round_num % len(game.users)

    start_user = session.query(User).filter(User.game == game, User.play_order == start_user_idx).first()
    curr_round.start_user = start_user
    
    session.add(curr_round)

    session.commit()

def prepare_new_round(game, engine):

    print(engine)

    session = Session(engine)

    if game.round_num >= game.max_cards:
        game.card_num -= 1
    else:
        game.card_num += 1
    
    game.round_num += 1

    game.game_stage = "G"

    generate_round(game, session)

    session.commit()

    session.close()


def generate_card_list():
    '''Returns list of cards'''

    cards = []

    for suit in suits:
        for rank in ranks:
            cards.append({'suit' : suit, 'rank' : rank})

    return cards

def start_play(game, curr_round, session):
    
    new_play = Play(play_num = 1, current_user = curr_round.start_user, round = curr_round, game = game)

    session.add(new_play)
    session.commit()

def next_play(game, curr_round, engine):

    session = Session(engine)

    play = session.query(Play).filter(Play.round == curr_round).order_by(Play.play_num.desc()).first()

    start_player = play.winner

    new_play = Play(play_num = len(round.plays) + 1, current_user = start_player, round = curr_round, game = game)

    session.add(new_play)
    session.commit()

    session.close()

def end_round(curr_round, game, session, engine):
    calculate_score(curr_round, game, session)

    if game.round_num == (game.max_cards * 2 - 1):
        game.game_stage = "F"
        #TODO Add thread to delete record after 24 hours
    else:
        game.game_stage = "R"
        print("start")
        t = threading.Timer(END_ROUND_WAIT_TIME, prepare_new_round, [game, engine])
    
    t.start()
    session.commit()


def calculate_score(curr_round, game, session):

    for guess in curr_round.guesses:
        num_wins = session.query(Play).filter(Play.round == curr_round, Play.winner == guess.user).count()

        if num_wins == guess.guess:
            score = 10 + num_wins * 5
        else:
            score = 0
        
        user_points = Round_point(points = score, user = guess.user, round = curr_round)

        session.add(user_points)
    
    session.commit()