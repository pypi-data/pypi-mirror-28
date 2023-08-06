import rethinkdb as R

from .base_models import BaseModel
from ..base import BaseTestCase


class OrmFeatureTest(BaseTestCase):

    def test_all(self):
        self.assertQueryEqual(
            BaseModel.all(),
            R.table(BaseModel._table)
        )

        self.assertQueryEqual(
            BaseModel.all(limit=5),
            R.table(BaseModel._table).limit(5)
        )

        self.assertQueryEqual(
            BaseModel.all(skip=5),
            R.table(BaseModel._table).skip(5)
        )

        self.assertQueryEqual(
            BaseModel.all(limit=5, skip=6),
            R.table(BaseModel._table).skip(6).limit(5)
        )

    def test_count(self):
        self.assertQueryEqual(
            BaseModel.count(),
            R.table(BaseModel._table).count()
        )

        self.assertQueryEqual(
            BaseModel.count(BaseModel.test_field_1 == '5'),
            R.table(BaseModel._table).filter(R.row['test_field_1'] == '5').count()
        )

    def test_sample(self):
        self.assertQueryEqual(
            BaseModel.sample(5),
            R.table(BaseModel._table).sample(5)
        )

        self.assertQueryEqual(
            BaseModel.sample(5, BaseModel.test_field_1 == '5'),
            R.table(BaseModel._table).filter(R.row['test_field_1'] == '5').sample(5)
        )
