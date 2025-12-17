from database import create_session
from database.classes import Topic, User

def save_topic(topic_str: str, user_id: int) -> None:
    session = create_session()

    user = session.query(User).filter(User.id == user_id).first()
    user.topics.append(Topic(title=topic_str))

    session.commit()
    session.close()


def delete_topic(topic_id: int) -> None:
    session = create_session()

    topic = session.query(Topic).filter(Topic.id == topic_id).first()
    session.delete(topic)

    session.commit()
    session.close()
