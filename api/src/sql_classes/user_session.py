from sqlalchemy import *
from sqlalchemy.orm import relationship
from src.sql_functions.base import Base

class User_session(Base):
    '''User session db'''
    __tablename__ = 'user_sessions'
    id = Column(Integer, primary_key=True)
    
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="sessions")