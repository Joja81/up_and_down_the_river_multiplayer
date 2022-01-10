

from requests import sessions
from sqlalchemy.sql.expression import desc
from src.error import InputError
from src.game import start_play
from src.sql_classes.guess_class import Guess
from src.sql_classes.hand_class import Hand
from src.sql_classes.round_class import Round

from src.sql_classes.user_class import User


def collect_cards(auth_user_id, session):
    print(auth_user_id)
    user = session.query(User).get(auth_user_id)
    game = user.game

    if game.game_stage != "G":
        raise InputError(description="Not in guessing stage")

    curr_round = session.query(Round).filter(Round.game == game, Round.round_num == game.round_num).first()

    hand = session.query(Hand).filter(Hand.round == curr_round, Hand.user == user).first()

    cards = []

    for card in hand.cards:
        cards.append({'suit' : card.suit, 'rank' : card.rank})
        
    
    trump = {'suit' : curr_round.trump_card_suit, 'rank' : curr_round.trump_card_rank}

    return {'cards' : cards, 'trump' : trump}

def get_guesses(auth_user_id, session):

    user = session.query(User).get(auth_user_id)
    game = user.game

    if game.game_stage in ["S", "F"]:
        raise InputError(description="Guesses have not been entered for this round")

    curr_round = session.query(Round).filter(Round.game == game, Round.round_num == game.round_num).first()

    guesses = []

    for guess in curr_round.guesses:
        guesses.append({'player_name' : guess.user.name, 'player_guess' : guess.guess})

    guessing_complete = False
    user_guess = False
    curr_guesser_name = None

    if game.game_stage == "G":
        curr_player_idx = (game.round_num + len(guesses)) % len(game.users)

        curr_guesser_name = session.query(User).filter(User.game == game, User.play_order == curr_player_idx).first().name

        if curr_guesser_name == user.name:
            user_guess = True
    else:
        guessing_complete = True
    
    return {'guesses' : guesses, 'current_guesser' : curr_guesser_name, 'user_guess' : user_guess, 'is_guessing_complete' : guessing_complete}

def give_guess(auth_user_id, guess, session):
    user = session.query(User).get(auth_user_id)
    game = user.game
    
    if game.game_stage != "G":
        raise InputError(description="Not in guessing stage")
    
    curr_round = session.query(Round).filter(Round.game == game, Round.round_num == game.round_num).first()

    curr_player_idx = (game.round_num + len(curr_round.guesses)) % len(game.users)

    if user.play_order != curr_player_idx:
        raise InputError(description="It is not users turn to guess")
    
    # Check limits

    if guess > curr_round.card_num or guess < 0:
        raise InputError(description="Guess is not in range between and including 0 and number of cards")
    
    # Check if last user

    if len(curr_round.guesses) + 1 == len(game.users):
        if sum_guesses(curr_round.guesses) + guess == curr_round.card_num:
            raise InputError(description="Last palyer can't give guess that causes sum of guesses to equal card num")
    
    # Save guess

    user_guess = Guess(guess = guess, user = user, game = game)
    curr_round.guesses.append(user_guess) # Have to add seperatly for end of guessing check

    session.add(user_guess)

    # End guessing if last person has guessed
    if len(curr_round.guesses) == len(game.users):
        game.game_stage = "P"
        start_play(game, curr_round, session)

    session.commit()

    return {}


def sum_guesses(guesses):
    '''Sums up the users guesses'''

    total = 0
    for guess in guesses:
        total += guess.guess
    
    return total