from sqlalchemy.sql.functions import current_date
from src.sql_classes.card_class import Card
from src.sql_classes.hand_class import Hand
from src.sql_classes.play_class import Play
from src.sql_classes.round_class import Round
from src.sql_classes.user_class import User
from src.error import InputError
from src.game import end_round, next_play, ranks
import threading as th

def get_curr_cards(auth_user_id, session):
    user = session.query(User).get(auth_user_id)
    game = user.game

    if game.game_stage != "P":
        raise InputError(description="Not in playing stage") 

    curr_round = session.query(Round).filter(Round.game == game, Round.round_num == game.round_num).first()

    user_hand = session.query(Hand).filter(Hand.round == curr_round, Hand.user == user).first()

    curr_cards = []

    for card in user_hand.cards:
        if not card.played:
            curr_cards.append({'suit' : card.suit, 'rank' : card.rank})
    
    trump = {'suit' : curr_round.trump_card_suit, 'rank' : curr_round.trump_card_rank}

    return {'cards' : curr_cards, 'trump' : trump}

def get_current_play(auth_user_id, session):
    user = session.query(User).get(auth_user_id)
    game = user.game

    if game.game_stage not in ["P", "R", "F"]:
        raise InputError(description="Not in playing stage") 

    curr_round = session.query(Round).filter(Round.game == game, Round.round_num == game.round_num).first()

    play = session.query(Play).filter(Play.round == curr_round).order_by(Play.play_num.desc()).first()

    cards = []

    for card in play.cards:
        cards.append({'suit' : card.suit, 'rank' : card.rank})
    
    return {
        'cards' : cards,
        'play_num' : play.play_num,
        'curr_user_turn' : play.current_user.name,
        'is_player_turn' : play.current_user == user and not play.completed,
        'is_finished' : play.completed
    }

def get_curr_wins(auth_user_id, session):
    user = session.query(User).get(auth_user_id)
    game = user.game

    if game.game_stage != "P":
        raise InputError(description="Not in playing stage") 

    curr_round = session.query(Round).filter(Round.game == game, Round.round_num == game.round_num).first()

    scores = []

    for user in game.users:
        num_wins = session.query(Play).filter(Play.round == curr_round, Play.winner == user).count()
        scores.append({'name' : user.name, 'score' : num_wins})
    
    return {'scores' : scores}

def give_play(auth_user_id, chosen_card, session):
    user = session.query(User).get(auth_user_id)
    game = user.game

    if game.game_stage != "P":
        raise InputError(description="Not in playing stage") 

    curr_round = session.query(Round).filter(Round.game == game, Round.round_num == game.round_num).first()

    play = session.query(Play).filter(Play.round == curr_round).order_by(Play.play_num.desc()).first()

    curr_cards = get_curr_cards(auth_user_id, session)

    if user != play.current_user or play.completed:
        raise InputError(description="Not user turn")

    if chosen_card not in curr_cards['cards']:
        raise InputError(description="User does not have this card in there hand")
    
    if len(play.cards) > 0:
        if chosen_card['suit'] != play.cards[0].suit:
            if check_user_not_have_suit(curr_cards['cards'], play.cards[0].suit):
                raise InputError(description="User has card of correct suit that they must play")
    card = session.query(Card).filter(Card.round == curr_round, Card.suit == chosen_card['suit'], Card.rank == chosen_card['rank']).first()

    card.play_order = len(play.cards)
    
    card.played = True

    play.cards.append(card)


    if len(play.cards) == len(game.users):
        played_suit = play.cards[0].suit

        highest_played_suit = play.cards[0]
        highest_played_trump  = None

        for played_card in play.cards[1:]:
            if played_card.suit == played_suit:
                if ranks.index(played_card.rank) > ranks.index(highest_played_suit.rank):
                    highest_played_suit  = played_card
            if played_card.suit == curr_round.trump_card_suit:
                if highest_played_trump == None or ranks.index(played_card.rank) > ranks.index(highest_played_trump.rank):
                    highest_played_trump = played_card
        
        winning_user = None

        if highest_played_trump != None:
            winning_user = highest_played_trump.hand.user
        else:
            winning_user = highest_played_suit.hand.user

        play.winner = winning_user
        play.completed = True

        if play.play_num < curr_round.card_num:
            th.Timer(5, next_play, [game, curr_round])
        else:
            end_round(curr_round, game, session)
    else:
        next_user = session.query(User).filter(User.game == game, User.play_order == user.play_order + 1).first()

        if next_user == None:
            next_user = session.query(User).filter(User.game == game, User.play_order == 0).first()

        play.current_user = next_user

    session.commit()

    return {}

def check_user_not_have_suit(curr_cards, suit):
    for card in curr_cards:
        if card['suit'] == suit:
            return True
    return False