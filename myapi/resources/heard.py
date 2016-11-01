from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base

from myapi.common.db import session
from myapi.resources.question import Question
from myapi.resources.user import User

Base = declarative_base()


class Heard(Base):
    __tablename__ = 'heard_user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer)
    user_id = Column(Integer)

    def __init__(self, question_id, user_id):
        self.question_id = question_id
        self.user_id = user_id

    def toJson(self):
        question = session.query(Question).filter(Question.id == self.question_id).first().toJson()
        return dict(id=self.id, question=question)


class HeardResource(object):
    def set_heard_user(self, question_id, user_id):
        heard = Heard(question_id, user_id)
        session.add(heard)
        session.commit()
        if heard:
            user = session.query(User).filter(User.id == user_id)
            user.update({'heard_num': User.heard_num + 1})
            session.commit()
            question = session.query(Question).filter(Question.id == question_id)
            question.update({'listener_num': Question.listener_num})
            session.commit()
        return heard

    def get_user_heard_questions(self, user_id, offset, size):
        res = session.query(Heard).filter(Heard.user_id == user_id).offset(offset).limit(size).all()
        question_list = []
        if res:
            for x in res:
                question_list.append(x.toJson())
        return question_list

    def check_user_heard_question(self, user_id, question_id):
        heard = session.query(Heard).filter(and_(Heard.user_id == user_id, Heard.question_id == question_id)).all()
        return heard
