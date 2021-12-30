import random
from src.sql_classes.card_class import Card
from src.sql_classes.hand_class import Hand
from src.sql_classes.play_class import Play
from src.sql_classes.round_class import Round
from src.sql_classes.user_class import User

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
            curr_card = Card(suit = card['suit'], rank = card['rank'])

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

def generate_card_list():
    '''Returns list of cards'''

    suits = ['C', 'D', 'H', 'S']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

    cards = []

    for suit in suits:
        for rank in ranks:
            cards.append({'suit' : suit, 'rank' : rank})

    return cards

def start_play(game, curr_round, session):
    
    new_play = Play(play_num = 1, current_user = curr_round.start_user, round = curr_round, game = game)

    session.add(new_play)
    session.commit()