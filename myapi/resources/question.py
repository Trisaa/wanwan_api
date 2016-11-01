import datetime
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import and_
from sqlalchemy.ext.declarative import declarative_base

from myapi.common.db import session
from myapi.resources.user import User

Base = declarative_base()


class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True, autoincrement=True)
    state = Column(Integer)
    content = Column(String(200))
    price = Column(Float)
    public = Column(Integer)
    listener_num = Column(Integer)
    voice_length = Column(Integer)
    voice_url = Column(String(100))
    create_time = Column(DateTime)
    ask_user_id = Column(Integer)
    answer_user_id = Column(Integer)

    def __init__(self, content, price, public, ask_user_id, answer_user_id, listener, time, state):
        self.content = content
        self.price = price
        self.public = public
        self.ask_user_id = ask_user_id
        self.answer_user_id = answer_user_id
        self.listener_num = listener
        self.create_time = time
        self.state = state

    def toJson(self):
        ask_user = session.query(User).filter(User.id == self.ask_user_id).first().toJson()
        answer_user = session.query(User).filter(User.id == self.answer_user_id).first().toJson()
        return dict(id=self.id, state=self.state, content=self.content
                    , price=self.price, public=self.public, listener_num=self.listener_num
                    , voice_length=self.voice_length, voice_url=self.voice_url
                    , create_time=self.create_time.strftime('%Y-%m-%d %H:%M:%S'), ask_user=ask_user
                    , answer_user=answer_user)


class QuestionResource(object):
    def create_question(self, **kwargs):
        now = datetime.datetime.now()
        now.strftime('%Y-%m-%d %H:%M:%S')
        question = Question(kwargs['content'], kwargs['price'], kwargs['public']
                            , kwargs['ask_uuid'], kwargs['answer_uuid']
                            , 0, now, 0)
        session.add(question)
        session.commit()
        if question:
            user = session.query(User).filter(User.id == question.ask_user_id)
            user.update({'ask_num': User.ask_num + 1})
            session.commit()
        return question

    def get_related_questions(self, type, user_id, offset, size):
        if type == 'history':
            res = session.query(Question).order_by(Question.create_time.desc()).filter(
                and_(Question.answer_user_id == user_id, Question.voice_url != None
                     , Question.public == 1)).offset(offset).limit(size).all()
        elif type == 'ask':
            res = session.query(Question).order_by(Question.create_time.desc()).filter(
                Question.ask_user_id == user_id).offset(offset).limit(size).all()
        elif type == 'answer':
            res = session.query(Question).order_by(Question.create_time.desc()).filter(
                Question.answer_user_id == user_id).offset(offset).limit(size).all()
        question_list = []
        if res:
            for x in res:
                question_list.append(x.toJson())
        return question_list

    def get_question_detail(self, id):
        question = session.query(Question).filter(Question.id == id).first()
        return question

    def get_hot_questions(self, offset, size):
        res = session.query(Question).order_by(Question.create_time.desc()).filter(
            and_(Question.public == 1, Question.voice_url != None)).offset(offset).limit(size).all()
        question_list = []
        if res:
            for x in res:
                question_list.append(x.toJson())
        return question_list

    def get_similar_questions(self, keyword, offset, size):
        res = session.query(Question).order_by(Question.create_time.desc()).filter(
            Question.content.ilike('%{}%'.format(keyword))).offset(offset).limit(size).all()
        question_list = []
        if res:
            for x in res:
                question_list.append(x.toJson())
        return question_list

    def answer_question(self, id, length, url):
        question = session.query(Question).filter(Question.id == id)
        if question:
            question.update({'voice_length': length})
            question.update({'voice_url': url})
            question.update({'state': 1})
            session.commit()
            user = session.query(User).filter(User.id == question.first().answer_user_id)
            user.update({'answer_num': User.answer_num + 1})
            user.update({'earning': User.earning + question.first().price})
            user.update({'income': User.income + question.first().price})
            session.commit()
            return question.first()
        else:
            return question
