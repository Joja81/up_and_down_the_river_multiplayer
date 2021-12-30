from sqlalchemy import *
from sqlalchemy.orm import relationship

from src.sql_functions.base import Base

class Hand(Base):
        '''Store for hand of user'''
        __tablename__ = 'hands'
        id = Column(Integer, primary_key=True)

        round_id = Column(Integer, ForeignKey("rounds.id"))
        round = relationship("Round")

        user_id = Column(Integer, ForeignKey("users.id"))
        user = relationship("User")