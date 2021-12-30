from sqlalchemy import *
from sqlalchemy.orm import relationship

from src.sql_functions.base import Base

class Game(Base):
        '''Store for game'''
        __tablename__ = 'games'
        # Make generation random
        id = Column(Integer, primary_key=True)

        time_start = Column(Integer)

        max_cards = Column(Integer)

        game_stage = Column(String(1)) # Stage of game, 'S' = starting, 'G' = guessing, 'P' = playing, 'F' = finished

        round_num = Column(Integer)

        card_num = Column(Integer)