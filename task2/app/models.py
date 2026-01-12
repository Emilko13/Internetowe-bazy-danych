from sqlalchemy import Column, Integer, String
from .database import Base

class User(Base):
    __tablename__ = 'sqlalchemy_users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
