import unittest

from anji_orm.model import Model
from anji_orm.fields import StringField
from anji_orm.syntax.query import QueryBoundStatement, Interval, QueryRow, EmptyQueryStatement


class T1(Model):

    _table = 'non_table'

    c1 = StringField()
    c2 = StringField()


class QueryMergeTest(unittest.TestCase):

    def test_equals_merge_short(self):
        self.assertEqual(T1.c1 == 5, (T1.c1 == 5) & (T1.c1.one_of(5, 6)))
        self.assertEqual(T1.c1 == 5, (T1.c1 == 5) & (T1.c1 == 5))
        self.assertEqual(T1.c1 == 5, (T1.c1 == 5) & (T1.c1 <= 5))
        self.assertEqual(T1.c1 == 5, (T1.c1 == 5) & (T1.c1 >= 5))
        self.assertEqual(T1.c1 == 5, (T1.c1 == 5) & (T1.c1 < 6))
        self.assertEqual(T1.c1 == 5, (T1.c1 == 5) & (T1.c1 > 4))
        self.assertEqual(T1.c1 == 5, (T1.c1 == 5) & (T1.c1 != 4))
        self.assertEqual(T1.c1 == 5, (T1.c1 == 5) & ((T1.c1 < 6) & (T1.c1 > 4)))

    def test_equals_merge_collection(self):
        self.assertEqual((T1.c1 == 5) & (T1.c2 == 4), (T1.c1 == 5) & (T1.c2 == 4) & (T1.c1.one_of(5, 6)))
        self.assertEqual((T1.c1 == 5) & (T1.c2 == 4), (T1.c1 == 5) & (T1.c2 == 4) & (T1.c1 == 5))
        self.assertEqual((T1.c1 == 5) & (T1.c2 == 4), (T1.c1 == 5) & (T1.c2 == 4) & (T1.c1 <= 5))
        self.assertEqual((T1.c1 == 5) & (T1.c2 == 4), (T1.c1 == 5) & (T1.c2 == 4) & (T1.c1 >= 5))
        self.assertEqual((T1.c1 == 5) & (T1.c2 == 4), (T1.c1 == 5) & (T1.c2 == 4) & (T1.c1 < 6))
        self.assertEqual((T1.c1 == 5) & (T1.c2 == 4), (T1.c1 == 5) & (T1.c2 == 4) & (T1.c1 > 4))
        self.assertEqual((T1.c1 == 5) & (T1.c2 == 4), (T1.c1 == 5) & (T1.c2 == 4) & (T1.c1 != 4))
        self.assertEqual((T1.c1 == 5) & (T1.c2 == 4), (T1.c1 == 5) & (T1.c2 == 4) & ((T1.c1 < 6) & (T1.c1 > 4)))

    def test_bound_merge_short(self):
        target_statement = QueryBoundStatement(QueryRow('c1'), Interval(4, 6, right_close=True))
        self.assertEqual(T1.c1.one_of(5, 6), target_statement & T1.c1.one_of(5, 6))
        # Without reducing bound
        self.assertEqual(target_statement, target_statement & (T1.c1 < 7))
        self.assertEqual(target_statement, target_statement & (T1.c1 <= 7))
        self.assertEqual(target_statement, target_statement & (T1.c1 > 4))
        self.assertEqual(target_statement, target_statement & (T1.c1 >= 4))
        # With reducing bounds
        target_statement1 = QueryBoundStatement(QueryRow('c1'), Interval(3, 6, right_close=True))
        self.assertEqual(target_statement, target_statement1 & (T1.c1 > 4))
        target_statement1 = QueryBoundStatement(QueryRow('c1'), Interval(4, 8, right_close=True))
        self.assertEqual(target_statement, target_statement1 & (T1.c1 <= 6))
        target_statement.right.left_close = True
        target_statement.right.right_close = False
        # Switch interval
        target_statement1 = QueryBoundStatement(QueryRow('c1'), Interval(3, 6, left_close=True))
        self.assertEqual(target_statement, target_statement1 & (T1.c1 >= 4))
        target_statement1 = QueryBoundStatement(QueryRow('c1'), Interval(4, 8, left_close=True))
        self.assertEqual(target_statement, target_statement1 & (T1.c1 < 6))
        # Merge with bound
        target_statement1 = QueryBoundStatement(QueryRow('c1'), Interval(3, 6, left_close=True))
        self.assertEqual(target_statement, target_statement & target_statement1)

    def test_isin_merge_short(self):
        target_statement = T1.c1.one_of(5, 6)
        self.assertEqual(target_statement, T1.c1.one_of(5, 6, 7) & target_statement)

        self.assertEqual(target_statement, target_statement & (T1.c1 >= 5))
        self.assertEqual(target_statement, target_statement & (T1.c1 > 4))
        self.assertEqual(target_statement, target_statement & (T1.c1 <= 6))
        self.assertEqual(target_statement, target_statement & (T1.c1 < 7))

    def test_le_merge_short(self):
        target_statement = T1.c1 <= 5

        self.assertEqual(target_statement, target_statement & (T1.c1 < 6))
        self.assertEqual(target_statement, target_statement & (T1.c1 <= 6))
        self.assertEqual(T1.c1 < 5, target_statement & (T1.c1 < 5))
        self.assertEqual(T1.c1 < 4, target_statement & (T1.c1 < 4))

        target_statement = QueryBoundStatement(T1.c1, Interval(4, 5, right_close=True))
        self.assertEqual(target_statement, (T1.c1 <= 5) & (T1.c1 > 4))
        target_statement.right.left_close = True
        self.assertEqual(target_statement, (T1.c1 <= 5) & (T1.c1 >= 4))

    def test_lt_merge_short(self):
        self.assertEqual(T1.c1 < 5, (T1.c1 < 5) & (T1.c1 < 6))

        target_statement = QueryBoundStatement(T1.c1, Interval(4, 5))
        self.assertEqual(target_statement, (T1.c1 < 5) & (T1.c1 > 4))
        target_statement.right.left_close = True
        self.assertEqual(target_statement, (T1.c1 < 5) & (T1.c1 >= 4))

    def test_ge_merge_short(self):
        self.assertEqual(T1.c1 >= 5, (T1.c1 >= 5) & (T1.c1 >= 4))
        self.assertEqual(T1.c1 >= 5, (T1.c1 >= 5) & (T1.c1 > 4))
        self.assertEqual(T1.c1 > 5, (T1.c1 > 5) & (T1.c1 >= 4))

    def test_gt_merge_short(self):
        self.assertEqual(T1.c1 > 6, (T1.c1 > 5) & (T1.c1 > 6))

    def test_ne_merge_short(self):
        self.assertEqual(T1.c1.one_of(5, 10), T1.c1.one_of(5, 10, 15) & (T1.c1 != 15))
        bound_statement = (T1.c1 >= 20) & (T1.c1 <= 40)
        self.assertEqual(bound_statement, bound_statement & (T1.c1 != 15))
        self.assertEqual(bound_statement, bound_statement & (T1.c1 != 35))


class QueryEmptyTest(unittest.TestCase):

    def test_eq_empty(self):
        target_statement = EmptyQueryStatement()
        self.assertEqual(target_statement, (T1.c1 == 7) & (T1.c1.one_of(5, 6)))
        self.assertEqual(target_statement, (T1.c1 == 7) & (T1.c1 == 5))
        self.assertEqual(target_statement, (T1.c1 == 7) & (T1.c1 <= 5))
        self.assertEqual(target_statement, (T1.c1 == 4) & (T1.c1 >= 5))
        self.assertEqual(target_statement, (T1.c1 == 7) & (T1.c1 < 6))
        self.assertEqual(target_statement, (T1.c1 == 4) & (T1.c1 > 4))
        self.assertEqual(target_statement, (T1.c1 == 4) & (T1.c1 != 4))
        self.assertEqual(target_statement, (T1.c1 == 8) & ((T1.c1 < 6) & (T1.c1 > 4)))

    def test_bound_empty(self):
        target_statement = EmptyQueryStatement()
        bound_statement = (T1.c1 >= 20) & (T1.c1 <= 40)
        self.assertEqual(target_statement, bound_statement & (T1.c1.one_of(5, 6)))
        self.assertEqual(target_statement, bound_statement & (T1.c1 == 5))
        self.assertEqual(target_statement, bound_statement & (T1.c1 <= 10))
        self.assertEqual(target_statement, bound_statement & (T1.c1 >= 50))
        self.assertEqual(target_statement, bound_statement & (T1.c1 < 10))
        self.assertEqual(target_statement, bound_statement & (T1.c1 > 45))
        self.assertEqual(target_statement, bound_statement & ((T1.c1 < 6) & (T1.c1 > 4)))

    def test_isin_empty(self):
        target_statement = EmptyQueryStatement()
        isin_statement = T1.c1.one_of(10, 15, 20)
        self.assertEqual(target_statement, isin_statement & (T1.c1.one_of(5, 6)))
        self.assertEqual(target_statement, isin_statement & (T1.c1 == 5))
        self.assertEqual(target_statement, isin_statement & (T1.c1 <= 5))
        self.assertEqual(target_statement, isin_statement & (T1.c1 >= 50))
        self.assertEqual(target_statement, isin_statement & (T1.c1 < 5))
        self.assertEqual(target_statement, isin_statement & (T1.c1 > 45))
        self.assertEqual(target_statement, isin_statement & (T1.c1 != 15) & (T1.c1 != 20) & (T1.c1 != 10))
        self.assertEqual(target_statement, isin_statement & ((T1.c1 < 6) & (T1.c1 > 4)))

    def test_le_empty(self):
        target_statement = EmptyQueryStatement()
        base_statement = T1.c1 <= 40
        self.assertEqual(target_statement, base_statement & (T1.c1.one_of(50, 60)))
        self.assertEqual(target_statement, base_statement & (T1.c1 == 50))
        self.assertEqual(target_statement, base_statement & (T1.c1 >= 50))
        self.assertEqual(target_statement, base_statement & (T1.c1 > 45))
        self.assertEqual(target_statement, base_statement & ((T1.c1 < 60) & (T1.c1 > 50)))

    def test_lt_empty(self):
        target_statement = EmptyQueryStatement()
        base_statement = T1.c1 < 40
        self.assertEqual(target_statement, base_statement & (T1.c1.one_of(50, 60)))
        self.assertEqual(target_statement, base_statement & (T1.c1 == 50))
        self.assertEqual(target_statement, base_statement & (T1.c1 >= 50))
        self.assertEqual(target_statement, base_statement & (T1.c1 > 45))
        self.assertEqual(target_statement, base_statement & ((T1.c1 < 60) & (T1.c1 > 50)))

    def test_ge_empty(self):
        target_statement = EmptyQueryStatement()
        base_statement = T1.c1 >= 40
        self.assertEqual(target_statement, base_statement & (T1.c1.one_of(5, 6)))
        self.assertEqual(target_statement, base_statement & (T1.c1 == 5))
        self.assertEqual(target_statement, base_statement & (T1.c1 <= 30))
        self.assertEqual(target_statement, base_statement & (T1.c1 < 30))
        self.assertEqual(target_statement, base_statement & ((T1.c1 < 6) & (T1.c1 > 4)))

    def test_gt_empty(self):
        target_statement = EmptyQueryStatement()
        base_statement = T1.c1 > 40
        self.assertEqual(target_statement, base_statement & (T1.c1.one_of(5, 6)))
        self.assertEqual(target_statement, base_statement & (T1.c1 == 5))
        self.assertEqual(target_statement, base_statement & (T1.c1 <= 30))
        self.assertEqual(target_statement, base_statement & (T1.c1 < 30))
        self.assertEqual(target_statement, base_statement & ((T1.c1 < 6) & (T1.c1 > 4)))

    def test_empty_and(self):
        self.assertEqual(EmptyQueryStatement(), EmptyQueryStatement() & EmptyQueryStatement())
