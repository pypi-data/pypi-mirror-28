# coding:utf-8
class stu(object):
    def __init__(self,n):
        self.name = n
    def say(self):
        print self.name
def ceshi(a):
    print a
    print __name__
if __name__ is "__main__":
    ceshi("aasd")