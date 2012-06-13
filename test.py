# coding=utf-8
import unittest
import bean
from dbutil import DB
class DbTest(unittest.TestCase):
    def setUp(self):
        #select and clear the db
        bean.db = DB("test")
        db = bean.db
        for dbname in db.collection_names():
            db[dbname].remove()
            
    def test_add_grat_bean(self):

        bm = bean.BeanManager()
        self.assertNotEquals(None,bm.add_gratitude_bean(content = u"我很快乐",tags=[u"快乐",u"我"]))

if __name__ == '__main__':
        unittest.main()
