import unittest

import rethinkdb as R

from anji_orm.utils import check_equals


class BaseTestCase(unittest.TestCase):

    def assertQueryEqual(self, first_query: R.RqlQuery, second_query: R.RqlQuery) -> None:  # pylint: disable=invalid-name
        if not check_equals(first_query, second_query):
            raise self.failureException(f"Query {str(first_query)} are not the same as query {str(second_query)}")
