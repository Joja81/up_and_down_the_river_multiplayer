
from sqlalchemy import *
from sqlalchemy.orm import relationship

from app import db

class Card(db.Model):
        '''Store for a card in a hand'''
        __tablename__ = 'cards'
        id = Column(Integer, primary_key=True)

        suit = Column(String(1))
        rank = Column(String(1))

        play_order = Column(Integer)

        played = Column(Boolean, default = False)

        hand_id = Column(Integer, ForeignKey("hands.id"))
        hand = relationship("Hand", back_populates="cards")

        play_id = Column(Integer, ForeignKey("plays.id"))
        play = relationship("Play", back_populates = "cards")

        round_id = Column(Integer, ForeignKey("rounds.id"))
        round = relationship("Round", back_populates = "cards")
        
class User_session(db.Model):
    '''User session db'''
    __tablename__ = 'user_sessions'
    id = Column(Integer, primary_key=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="sessions")
    

class Guess(db.Model):
    '''stores user guesses'''
    __tablename__= 'guesses'
    id = Column(Integer, primary_key = True)

    guess = Column(Integer)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="guesses")

    round_id = Column(Integer, ForeignKey('rounds.id'))
    round = relationship('Round', back_populates="guesses")

    game_id = Column(Integer, ForeignKey('games.id'))
    game = relationship('Game', back_populates="guesses")


class Hand(db.Model):
        '''Store for hand of user'''
        __tablename__ = 'hands'
        id = Column(Integer, primary_key=True)

        round_id = Column(Integer, ForeignKey("rounds.id"))
        round = relationship("Round", back_populates= "hands")

        user_id = Column(Integer, ForeignKey("users.id"))
        user = relationship("User", back_populates= "hands")
        
        cards = relationship("Card", order_by=Card.id, cascade="all, delete", back_populates= "hand")
        
class Play(db.Model):
        '''Store for an individual play of a round'''
        __tablename__ = 'plays'
        id = Column(Integer, primary_key=True)

        play_num = Column(Integer)
        
        round_status = Column(String(1), default = "p") # Status of play, p = playing, w = waiting, f = finish
        
        wait_end = Column(Integer)        

        current_user_id = Column(Integer, ForeignKey("users.id"))
        current_user = relationship("User", foreign_keys=current_user_id)

        winner_id = Column(Integer, ForeignKey("users.id"))
        winner = relationship("User", foreign_keys=winner_id)

        round_id = Column(Integer, ForeignKey("rounds.id"))
        round = relationship("Round", back_populates="plays")

        game_id = Column(Integer, ForeignKey("games.id"))
        game = relationship("Game", back_populates= "plays")
        
        cards = relationship("Card", order_by=Card.play_order, cascade="all, delete", back_populates= "play")

class Round_point(db.Model):
        '''Store for points user gained in round'''
        __tablename__ = 'round_points'
        id = Column(Integer, primary_key=True)

        points = Column(Integer)

        user_id = Column(Integer, ForeignKey("users.id"))
        user = relationship("User", back_populates="round_points")

        round_id = Column(Integer, ForeignKey("rounds.id"))
        round = relationship("Round", back_populates="round_points")


class Round(db.Model):
        '''Store for round'''
        __tablename__ = 'rounds'
        id = Column(Integer, primary_key=True)

        round_num = Column(Integer)
        card_num = Column(Integer)

        trump_card_suit = Column(String(1)) # Stores suit of trump
        trump_card_rank = Column(String(1)) # Stores rank of trump

        start_user_id = Column(Integer, ForeignKey("users.id"))
        start_user = relationship("User")

        game_id = Column(Integer, ForeignKey("games.id"))
        game = relationship("Game")
        
        guesses = relationship("Guess", order_by=Guess.id, cascade="all, delete", back_populates= "round")
        
        hands = relationship("Hand", order_by=Hand.id, cascade="all, delete", back_populates = "round")
        
        plays = relationship("Play", order_by=Play.play_num, cascade="all, delete", back_populates="round")

        round_points = relationship("Round_point", order_by=Round_point.id, cascade="all, delete", back_populates="round")
   
        cards = relationship("Card", order_by= Card.id, cascade = "all, delete", back_populates="round")
   
class User(db.Model):
        '''Store for user'''
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)

        name = Column(String(256))

        is_owner = Column(Boolean, default=False)

        play_order = Column(Integer)

        game_id = Column(Integer, ForeignKey("games.id"))
        game = relationship("Game", back_populates="users")
        
        sessions = relationship("User_session", order_by=User_session.id, back_populates= "user")

        guesses = relationship("Guess", order_by=Guess.id, cascade="all, delete", back_populates="user")
    
        hands = relationship("Hand", order_by=Hand.id, cascade="all, delete", back_populates = "user")

        round_points = relationship("Round_point", order_by=Round_point.id, cascade="all, delete", back_populates= "user")

class Game(db.Model):
        '''Store for game'''
        __tablename__ = 'games'
        # Make generation random
        id = Column(Integer, primary_key=True)

        time_start = Column(Integer)

        max_cards = Column(Integer)

        game_stage = Column(String(1)) # Stage of game, 'S' = starting, 'G' = guessing, 'P' = playing, 'R' = Results, 'F' = Finished

        new_round_time = Column(Integer)

        round_num = Column(Integer)

        card_num = Column(Integer)
        
        users = relationship("User", order_by=User.id, cascade="all, delete", back_populates="game")

        guesses = relationship("Guess", order_by=Guess.id, cascade="all, delete", back_populates="game")

        plays = relationship("Play", order_by=Play.id, cascade="all, delete", back_populates= "game")
