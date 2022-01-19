from sqlalchemy import *
from sqlalchemy.orm import relationship

from src.sql_functions.base import Base

class User(Base):
        '''Store for user'''
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)

        name = Column(String(256))

        is_owner = Column(Boolean, default=False)

        play_order = Column(Integer)

        game_id = Column(Integer, ForeignKey("games.id"))
        game = relationship("Game", back_populates="users")