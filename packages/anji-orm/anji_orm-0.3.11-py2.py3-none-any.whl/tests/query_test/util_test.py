import unittest

from anji_orm.model import Model
from anji_orm.fields import StringField


class T1(Model):

    _table = 'non_table'

    c1 = StringField()
    c2 = StringField()


class QueryMergeTest(unittest.TestCase):

    def test_check_complicated(self):
        self.assertTrue((T1.c1 == T1.c2).complicated)
        self.assertFalse((T1.c1 == '5').complicated)
        self.assertFalse(((T1.c1 == '5') & (T1.c1 == '6')).complicated)
        self.assertFalse(((T1.c1 == '5') & (T1.c2 == '6')).complicated)
        self.assertTrue(((T1.c1 == T1.c2) & (T1.c2 == '6')).complicated)
        self.assertTrue(((T1.c1 == T1.c2) & (T1.c1 == '6')).complicated)
