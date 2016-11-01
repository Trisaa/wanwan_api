from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from myapi.config import Config

Session = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(Config.SQLALCHEMY_DATABASE_URI))

session = scoped_session(Session)
