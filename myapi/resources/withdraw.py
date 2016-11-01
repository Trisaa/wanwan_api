import datetime
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

from myapi.common.db import session

Base = declarative_base()


class Withdraw(Base):
    __tablename__ = 'withdraw'
    id = Column(Integer, primary_key=True, autoincrement=True)
    paypal = Column(String(45))
    user_id = Column(Integer)
    time = Column(DateTime)
    dealed = Column(Integer)

    def __init__(self, paypal, user_id, time, dealed):
        self.paypal = paypal
        self.user_id = user_id
        self.time = time
        self.dealed = dealed

    def toJson(self):
        return dict(id=self.id, paypal=self.paypal, user_id=self.user_id
                    , time=self.time, dealed=self.dealed)


class WithdrawResource(object):
    def create_withdraw(self, paypal, user_id):
        now = datetime.datetime.now()
        now.strftime('%Y-%m-%d %H:%M:%S')
        withdraw = Withdraw(paypal, user_id, now, 0)
        session.add(withdraw)
        session.commit()
        return withdraw
