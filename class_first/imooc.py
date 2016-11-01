from __future__ import unicode_literals
import time
import functools


def performance(f):
    def fn(*args, **kw):
        t1 = time.time()
        r = f(*args, **kw)
        t2 = time.time()
        print 'call %s() in %fs' % (f.__name__, (t2 - t1))
        return r

    return fn


@performance
def fac(n):
    return reduce(lambda x, y: x * y, range(1, n + 1))


sorted_ignore = functools.partial(sorted, cmp=lambda x, y: cmp(x.upper(), y.upper()))

# print sorted_ignore(['bob', 'Zoo', 'Credit'])

s = 'am i an unicode?'
#print isinstance(s, unicode)


class Person(object):
    def __init__(self, name, age, gender, score):
        self.name = name
        self.age = age
        self.gender = gender
        self.__score = score

class Teacher(Person):
    def __init__(self,name,age,gender,score,course):
        super(Teacher, self).__init__(name,age,gender,score)
        self.course = course

laowang = Teacher('XiaoMing', 12, 'Female', 100,'math')
print laowang.course