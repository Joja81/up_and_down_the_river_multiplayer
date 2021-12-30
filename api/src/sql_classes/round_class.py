from sqlalchemy import *
from sqlalchemy.orm import relation, relationship

from src.sql_functions.base import Base

class Round(Base):
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