from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from soloask_api.common.config import SQLALCHEMY_DATABASE_URI

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

    def __init__(self, third_uuid, username, icon, device_token):
        self.third_uuid = third_uuid
        self.username = username
        self.icon = icon
        self.device_token = device_token

    def to_json(self):
        return dict(id=self.id, username=self.username, icon=self.icon, title=self.title
                    , introduction=self.introduction, price=self.price, income=self.income
                    , device_token=self.device_token, ask_num=self.ask_num, answer_num=self.answer_num
                    , heard_num=self.heard_num, earning=self.earning, third_party_uuid=self.third_party_uuid)


if __name__ == "__main__":
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
