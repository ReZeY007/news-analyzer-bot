from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .classes import Base


Session = None

def init_database():
    global Session
    if Session:
        return

    engine = create_engine('sqlite:///database/topics.db', echo = False)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)


def create_session():
    global Session
    return Session()