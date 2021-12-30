from sqlalchemy.sql.functions import current_date
from src.sql_classes.hand_class import Hand
from src.sql_classes.play_class import Play
from src.sql_classes.round_class import Round
from src.sql_classes.user_class import User
from src.error import InputError

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

    if game.game_stage not in ["P", "F"]:
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
        'is_player_turn' : play.current_user == user,
        'is_finished' : play.completed
    }

def get_current_play(auth_user_id, session):
    user = session.query(User).get(auth_user_id)
    game = user.game

    if game.game_stage == "P":
        raise InputError(description="Not in playing stage") 

    curr_round = session.query(Round).filter(Round.game == game, Round.round_num == game.round_num).first()

    for play in curr_round.plays:
        if play.completed