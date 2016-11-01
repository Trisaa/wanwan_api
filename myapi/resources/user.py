from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

from myapi.common.db import session

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(45), unique=True)
    icon = Column(String(200))
    title = Column(String(36))
    introduction = Column(String(200))
    price = Column(Float)
    income = Column(Float)
    device_token = Column(String(100))
    ask_num = Column(Integer)
    answer_num = Column(Integer)
    heard_num = Column(Integer)
    earning = Column(Float)
    third_party_uuid = Column(String(50))

    def __init__(self, third_party_uuid, username, icon, device_token):
        self.third_party_uuid = third_party_uuid
        self.username = username
        self.icon = icon
        self.device_token = device_token
        self.title = 'Good guys'
        self.introduction = 'Ask me everything'
        self.price = 0.99
        self.income = 0
        self.ask_num = 0
        self.answer_num = 0
        self.heard_num = 0
        self.earning = 0

    def toJson(self):
        return dict(id=self.id, username=self.username, icon=self.icon, title=self.title
                    , introduction=self.introduction, price=self.price, income=self.income
                    , device_token=self.device_token, ask_num=self.ask_num, answer_num=self.answer_num
                    , heard_num=self.heard_num, earning=self.earning, third_party_uuid=self.third_party_uuid)

    def __repr__(self):
        return "User: username=%s,third_party_uuid=%s" % (self.username, self.third_party_uuid)


class UserResource(object):
    def login(self, third_party_uuid, username, icon, device_token):
        exist_user_data = session.query(User).filter(User.third_party_uuid == third_party_uuid).first()
        if exist_user_data:
            return exist_user_data
        new_user_data = User(third_party_uuid, username, icon, device_token)
        session.add(new_user_data)
        session.commit()
        return new_user_data

    def get_user_info(self, user_id):
        user_data = session.query(User).filter(User.id == user_id).first()
        return user_data

    def update_user_info(self, user_id, **kwargs):
        user_data = session.query(User).filter(User.id == user_id)
        if user_data:
            for key in kwargs:
                user_data.update({key: kwargs[key]})
            session.commit()
            return user_data.first()
        else:
            return user_data

    def get_user_list(self, offset, size):
        res = session.query(User).order_by(User.answer_num.desc()).offset(offset).limit(size).all()
        user_list = []
        if res:
            for x in res:
                user_list.append(x.toJson())
        return user_list

    def get_similar_users(self, keyword, offset, size):
        res = session.query(User).order_by(User.answer_num.desc()).filter(
            User.username.ilike('%{}%'.format(keyword))).offset(
            offset).limit(size).all()
        user_list = []
        if res:
            for x in res:
                user_list.append(x.toJson())
        return user_list
