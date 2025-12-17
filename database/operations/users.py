from database import create_session
from database.classes import User, Topic


def save_user(user_id: int) -> None:
    session = create_session()
    usr = session.query(User).filter(User.id == user_id).first()
    
    if usr:
        session.close()
        return

    user = User(id = user_id)
    session.add(user)
    
    session.commit()
    session.close()


def get_user_topics(user_id: int) -> list[Topic]:
    session = create_session()
    
    user = session.query(User).filter(User.id == user_id).first()
    topics = user.topics

    if len(topics) == 0:
        raise Exception("User doesn't have topics")

    session.close()

    return topics