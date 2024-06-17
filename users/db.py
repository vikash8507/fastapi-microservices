import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


POSTGRESQL_USER = os.environ.get("POSTGRESQL_USER")
POSTGRESQL_PASSWORD = os.environ.get("POSTGRESQL_PASSWORD")
POSTGRESQL_DB = os.environ.get("POSTGRESQL_DB")
POSTGRESQL_HOST = os.environ.get("POSTGRESQL_HOST")
POSTGRESQL_PORT = int(os.environ.get("POSTGRESQL_PORT"))
SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:{POSTGRESQL_PORT}/{POSTGRESQL_DB}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()

Base = declarative_base()
