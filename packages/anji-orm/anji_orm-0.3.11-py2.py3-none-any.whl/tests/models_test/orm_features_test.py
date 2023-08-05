import unittest

import rethinkdb as R

from .base_models import BaseModel


class OrmFeatureTest(unittest.TestCase):

    def test_all(self):
        self.assertEqual(
            BaseModel.all().build(),
            R.table(BaseModel._table).build()
        )

        self.assertEqual(
            BaseModel.all(limit=5).build(),
            R.table(BaseModel._table).limit(5).build()
        )

        self.assertEqual(
            BaseModel.all(skip=5).build(),
            R.table(BaseModel._table).skip(5).build()
        )

        self.assertEqual(
            BaseModel.all(limit=5, skip=6).build(),
            R.table(BaseModel._table).skip(6).limit(5).build()
        )

    def test_count(self):
        self.assertEqual(
            BaseModel.count().build(),
            R.table(BaseModel._table).count().build()
        )

        self.assertEqual(
            BaseModel.count(BaseModel.test_field_1 == '5').build(),
            R.table(BaseModel._table).filter(R.row['test_field_1'] == '5').count().build()
        )

    def test_sample(self):
        self.assertEqual(
            BaseModel.sample(5).build(),
            R.table(BaseModel._table).sample(5).build()
        )

        self.assertEqual(
            BaseModel.sample(5, BaseModel.test_field_1 == '5').build(),
            R.table(BaseModel._table).filter(R.row['test_field_1'] == '5').sample(5).build()
        )
