from sqlalchemy import *
from sqlalchemy.orm import relation, relationship

from src.sql_functions.base import Base

class Round_point(Base):
        '''Store for points user gained in round'''
        __tablename__ = 'round_points'
        id = Column(Integer, primary_key=True)

        points = Column(Integer)

        user_id = Column(Integer, ForeignKey("users.id"))
        user = relationship("User", back_populates="round_points")

        round_id = Column(Integer, ForeignKey("rounds.id"))
        round = relationship("Round", back_populates="round_points")