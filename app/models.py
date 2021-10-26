from sqlalchemy import Integer, String
from sqlalchemy.sql.schema import Column
from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    hash = Column(String, nullable=False)
    telegram_id = Column(String, nullable=True)