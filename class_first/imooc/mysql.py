import MySQLdb


class TransferMoney(object):
    def __init__(self, conn):
        self.conn = conn

    def check_acct_available(self, acctid):
        cursor = self.conn.cursor()
        try:
            sql = "select * from account where acctid=%s" % acctid
            cursor.execute(sql)
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception("account %s doesn't exist" % acctid)
        finally:
            cursor.close()

    def has_enough_money(self, acctid, money):
        cursor = self.conn.cursor()
        try:
            sql = "select * from account where acctid=%s and money>%s" % (acctid, money)
            cursor.execute(sql)
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception("account %s doesn't have enough money" % acctid)
        finally:
            cursor.close()

    def reduce_money(self, acctid, money):
        cursor = self.conn.cursor()
        try:
            sql = "update account set money = money-%s where acctid=%s" % (money, acctid)
            cursor.execute(sql)
            if cursor.rowcount != 1:
                raise Exception("account %s failed to reduce money" % acctid)
        finally:
            cursor.close()

    def add_money(self, acctid, money):
        cursor = self.conn.cursor()
        try:
            sql = "update account set money = money+%s where acctid=%s" % (money, acctid)
            cursor.execute(sql)
            if cursor.rowcount != 1:
                raise Exception("account %s failed to add money" % acctid)
        finally:
            cursor.close()

    def transfer(self, source_accid, target_accid, money):
        try:
            self.check_acct_available(source_accid)
            self.check_acct_available(target_accid)
            self.has_enough_money(source_accid, money)
            self.reduce_money(source_accid, money)
            self.add_money(target_accid, money)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e


if __name__ == "__main__":
    source_accid = 1
    target_accid = 2
    money = 100

    db = MySQLdb.connect("localhost", "root", "lebron", "testdb")
    tr_money = TransferMoney(db)

    try:
        tr_money.transfer(source_accid, target_accid, money)
    except Exception as e:
        print "Something wrong\n" + str(e)
    finally:
        db.close()
