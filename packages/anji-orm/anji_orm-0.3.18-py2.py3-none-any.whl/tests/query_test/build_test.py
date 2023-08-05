import unittest

import rethinkdb as R

from anji_orm.model import Model
from anji_orm.fields import StringField
from anji_orm.syntax.parse import RethinkDBQueryParser


class T1(Model):

    _table = 'non_table'

    c1 = StringField(secondary_index=True)
    c2 = StringField(secondary_index=True)
    c3 = StringField()
    c4 = StringField(secondary_index=True)


class BaseQuerySecondaryIndexTest(unittest.TestCase):

    def test_simple_build(self):
        self.assertEqual(
            R.table('non_table').get_all('a1', 'a2', index='c2').build(),
            RethinkDBQueryParser.build_query(T1, T1.c2.one_of('a1', 'a2')).build()
        )

        self.assertEqual(
            R.table('non_table').get_all('a1', index='c2').build(),
            RethinkDBQueryParser.build_query(T1, T1.c2 == 'a1').build()
        )

        self.assertEqual(
            R.table('non_table').between('a1', R.maxval, index='c2', left_bound='open', right_bound='open').build(),
            RethinkDBQueryParser.build_query(T1, T1.c2 > 'a1').build()
        )

        self.assertEqual(
            R.table('non_table').between('a1', R.maxval, index='c2', left_bound='closed', right_bound='open').build(),
            RethinkDBQueryParser.build_query(T1, T1.c2 >= 'a1').build()
        )

        self.assertEqual(
            R.table('non_table').between(R.minval, 'a1', index='c2', left_bound='open', right_bound='open').build(),
            RethinkDBQueryParser.build_query(T1, T1.c2 < 'a1').build()
        )

        self.assertEqual(
            R.table('non_table').between(R.minval, 'a1', index='c2', left_bound='open', right_bound='closed').build(),
            RethinkDBQueryParser.build_query(T1, T1.c2 <= 'a1').build()
        )

        self.assertEqual(
            R.table('non_table').between('a2', 'a1', index='c2', left_bound='closed', right_bound='closed').build(),
            RethinkDBQueryParser.build_query(T1, (T1.c2 <= 'a1') and (T1.c2 >= 'a2')).build()
        )

        self.assertEqual(
            R.table('non_table').between('a2', 'a1', index='c2', left_bound='closed', right_bound='open').build(),
            RethinkDBQueryParser.build_query(T1, (T1.c2 < 'a1') and (T1.c2 >= 'a2')).build()
        )

        self.assertEqual(
            R.table('non_table').between('a2', 'a1', index='c2', left_bound='open', right_bound='closed').build(),
            RethinkDBQueryParser.build_query(T1, (T1.c2 <= 'a1') and (T1.c2 > 'a2')).build()
        )

        self.assertEqual(
            R.table('non_table').between('a2', 'a1', index='c2', left_bound='open', right_bound='open').build(),
            RethinkDBQueryParser.build_query(T1, (T1.c2 < 'a1') and (T1.c2 > 'a2')).build()
        )

    def test_with_not_index_build(self):

        self.assertEqual(
            R.table('non_table').get_all('a1', 'a2', index='c2').filter(R.row['c3'] < '5').build(),
            RethinkDBQueryParser.build_query(T1, (T1.c2.one_of('a1', 'a2')) & (T1.c3 < 5)).build()
        )


class BaseQuerySimpleFieldsTest(unittest.TestCase):

    def test_simple_build(self):
        rethinkdb_list = R.expr(['a1', 'a2'])
        row = R.row['c3']

        self.assertEqual(
            R.table('non_table').filter(lambda doc: rethinkdb_list.contains(doc['c3'])).build(),
            RethinkDBQueryParser.build_query(T1, T1.c3.one_of('a1', 'a2')).build()
        )

        self.assertEqual(
            R.table('non_table').filter(row == 'a1').build(),
            RethinkDBQueryParser.build_query(T1, T1.c3 == 'a1').build()
        )

        self.assertEqual(
            R.table('non_table').filter(row > 'a1').build(),
            RethinkDBQueryParser.build_query(T1, T1.c3 > 'a1').build()
        )

        self.assertEqual(
            R.table('non_table').filter(row >= 'a1').build(),
            RethinkDBQueryParser.build_query(T1, T1.c3 >= 'a1').build()
        )

        self.assertEqual(
            R.table('non_table').filter(row < 'a1').build(),
            RethinkDBQueryParser.build_query(T1, T1.c3 < 'a1').build()
        )

        self.assertEqual(
            R.table('non_table').filter(row <= 'a1').build(),
            RethinkDBQueryParser.build_query(T1, T1.c3 <= 'a1').build()
        )

        self.assertEqual(
            R.table('non_table').filter((row <= 'a1') & (row >= 'a2')).build(),
            RethinkDBQueryParser.build_query(T1, (T1.c3 <= 'a1') and (T1.c3 >= 'a2')).build()
        )

        self.assertEqual(
            R.table('non_table').filter((row < 'a1') & (row >= 'a2')).build(),
            RethinkDBQueryParser.build_query(T1, (T1.c3 < 'a1') and (T1.c3 >= 'a2')).build()
        )

        self.assertEqual(
            R.table('non_table').filter((row <= 'a1') & (row > 'a2')).build(),
            RethinkDBQueryParser.build_query(T1, (T1.c3 <= 'a1') and (T1.c3 > 'a2')).build()
        )

        self.assertEqual(
            R.table('non_table').filter((row < 'a1') & (row > 'a2')).build(),
            RethinkDBQueryParser.build_query(T1, (T1.c3 < 'a1') and (T1.c3 > 'a2')).build()
        )
