from src.sql_functions.base import Base
from sqlalchemy import *
from sqlalchemy.orm import relation, relationship

class Guess(Base):
    '''stores user guesses'''
    __tablename__= 'guesses'
    id = Column(Integer, primary_key = True)

    guess = Column(Integer)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User")

    round_id = Column(Integer, ForeignKey('rounds.id'))
    round = relationship('Round')

    game_id = Column(Integer, ForeignKey('games.id'))
    game = relationship('Game')