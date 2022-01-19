from sqlalchemy import *
from sqlalchemy.orm import relationship

from src.sql_functions.base import Base

class Play(Base):
        '''Store for an individual play of a round'''
        __tablename__ = 'plays'
        id = Column(Integer, primary_key=True)

        play_num = Column(Integer)

        completed = Column(Boolean, default=False)

        current_user_id = Column(Integer, ForeignKey("users.id"))
        current_user = relationship("User", foreign_keys=current_user_id)

        winner_id = Column(Integer, ForeignKey("users.id"))
        winner = relationship("User", foreign_keys=winner_id)

        round_id = Column(Integer, ForeignKey("rounds.id"))
        round = relationship("Round", back_populates="plays")

        game_id = Column(Integer, ForeignKey("games.id"))
        game = relationship("Game", back_populates= "plays")