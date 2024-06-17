from db import metadata, engine, Base
from sqlalchemy import Table

user_table = Table('users', metadata, autoload_with=engine)
class User(Base):
    __table__ = user_table


token_table = Table('tokens', metadata, autoload_with=engine)
class Token(Base):
    __table__ = token_table
