from sqlalchemy import *
from sqlalchemy.orm import relationship

from src.sql_functions.base import Base

class Card(Base):
        '''Store for a card in a hand'''
        __tablename__ = 'cards'
        id = Column(Integer, primary_key=True)

        suit = Column(String(1))
        rank = Column(String(1))

        play_order = Column(Integer)

        played = Column(Boolean, default = False)

        hand_id = Column(Integer, ForeignKey("hands.id"))
        hand = relationship("Hand")

        play_id = Column(Integer, ForeignKey("plays.id"))
        play = relationship("Play")

        round_id = Column(Integer, ForeignKey("rounds.id"))
        round = relationship("Round")