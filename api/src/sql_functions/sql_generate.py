from sqlalchemy.engine import create_engine
from sqlalchemy.orm import relation, relationship
from src.sql_functions.base import Base

 
def generate_engine():  
    """Creates engine and loads database classes and returns engine"""
   
    # Load classes for DB

    from src.sql_classes.game_class import Game
    from src.sql_classes.user_class import User
    from src.sql_classes.user_session import User_session
    from src.sql_classes.guess_class import Guess
    from src.sql_classes.round_class import Round
    from src.sql_classes.hand_class import Hand
    from src.sql_classes.card_class import Card
    from src.sql_classes.play_class import Play
    from src.sql_classes.round_points_class import Round_point

    # Create relationships
    User.sessions = relationship("User_session", order_by=User_session.id)
    
    Game.users = relationship("User", order_by=User.id)

    User.guesses = relationship("Guess", order_by=Guess.id)
    Round.guesses = relationship("Guess", order_by=Guess.id)
    Game.guesses = relationship("Guess", order_by=Guess.id)

    Round.hands = relationship("Hand", order_by=Hand.id)
    User.hands = relationship("Hand", order_by=Hand.id)

    Hand.cards = relationship("Card", order_by=Card.id)
    Play.cards = relationship("Card", order_by=Card.play_order)

    Game.plays = relationship("Play", order_by=Play.id)
    Round.plays = relationship("Play", order_by=Play.play_num)

    Round.round_points = relationship("Round_point", order_by=Round_point.id)
    User.round_points = relationship("Round_point", order_by=Round_point.id)

    # Create engine
    engine = create_engine("sqlite:///up_and_down_the_river.db")
    Base.metadata.create_all(engine)

    return engine