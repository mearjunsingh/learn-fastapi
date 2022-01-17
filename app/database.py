from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'sqlite:///./db.sqlite3'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

sessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()