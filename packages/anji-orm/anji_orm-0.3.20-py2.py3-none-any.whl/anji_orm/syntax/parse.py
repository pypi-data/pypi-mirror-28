from itertools import product, starmap
from typing import overload, List, Dict, Optional, Tuple, ValuesView

import rethinkdb as R

from .query import QueryStatementsCollection, QueryStatement, EmptyQueryStatement, StatementType, Interval

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.3.20"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = ['RethinkDBQueryParser', 'QueryBuildException']


class QueryBuildException(Exception):

    """
    Exception on query building
    """


class RethinkDBQueryParser:

    @overload
    @classmethod
    def index_bounds(cls, statements: ValuesView[QueryStatement]) -> Optional[Tuple[bool, bool]]:
        pass

    @overload
    @classmethod
    def index_bounds(cls, statements: ValuesView[QueryStatement]) -> Optional[bool]:  # pylint: disable=function-redefined
        pass

    @classmethod
    def index_bounds(cls, statements):  # pylint: disable=function-redefined,too-many-branches
        right_close = None
        left_close = None
        bound_statements = [
            StatementType.bound, StatementType.ge, StatementType.gt,
            StatementType.le, StatementType.lt
        ]
        for statement in filter(lambda x: x.statement_type in bound_statements, statements):
            if statement.statement_type == StatementType.le and right_close is None or right_close:
                right_close = True
            elif statement.statement_type == StatementType.lt and right_close is None or not right_close:
                right_close = False
            elif statement.statement_type == StatementType.ge and left_close is None or left_close:
                left_close = True
            elif statement.statement_type == StatementType.gt and left_close is None or not left_close:
                left_close = False
            elif statement.statement_type == StatementType.bound:
                if left_close is None or left_close == statement.right.left_close:
                    left_close = statement.right.left_close
                else:
                    return None
                if right_close is None or right_close == statement.right.right_close:
                    right_close = statement.right.right_close
                else:
                    return None
            else:
                return None
        if right_close is None and left_close is None:
            return False
        return left_close, right_close

    @classmethod
    def wrap_bound(cls, bound: bool) -> str:
        return 'closed' if bound else 'open'

    @classmethod
    def wrap_bounds(cls, index_bounds: Tuple[bool, bool], default_value: bool) -> Tuple[str, str]:
        return cls.wrap_bound(index_bounds[0] or default_value), cls.wrap_bound(index_bounds[1] or default_value)

    @classmethod
    def secondary_indexes_query(  # pylint: disable=too-many-branches,too-many-locals
            cls, search_query: R.RqlQuery, selected_index: str, statement_dict: Dict[str, QueryStatement]) -> R.RqlQuery:
        # According to https://github.com/python/mypy/issues/328
        splited_index = selected_index.split(':')
        index_bounds = cls.index_bounds((statement_dict[field] for field in splited_index))  # type: ignore
        isin_used = False
        if index_bounds is None:
            raise QueryBuildException("Cannot build query: inconsistency bounds for indexes")
        left_filter: List[List] = [[]]
        right_filter: List[List] = [[]]
        for statement_field in sorted(statement_dict.keys()):
            if statement_field in splited_index:
                statement: QueryStatement = statement_dict.get(statement_field)
                if statement.statement_type == StatementType.isin:
                    isin_used = True
                    if len(left_filter) == 1 and not left_filter[0]:
                        left_filter = [statement.right]
                        right_filter = [statement.right]
                    else:
                        left_filter = list(starmap(lambda base, new_value: base + [new_value], product(left_filter, statement.right)))
                        right_filter = list(starmap(lambda base, new_value: base + [new_value], product(right_filter, statement.right)))
                else:
                    new_left_filter = None
                    new_right_filter = None
                    if statement.statement_type in [StatementType.ge, StatementType.gt]:
                        new_left_filter = statement.right
                        new_right_filter = R.maxval
                    elif statement.statement_type in [StatementType.le, StatementType.lt]:
                        new_right_filter = statement.right
                        new_left_filter = R.minval
                    elif statement.statement_type == StatementType.eq:
                        new_right_filter = statement.right
                        new_left_filter = statement.right
                    elif statement.statement_type == StatementType.bound:
                        new_left_filter = statement.right.left_bound
                        new_right_filter = statement.right.right_bound
                    for filter_list in left_filter:
                        filter_list.append(new_left_filter)
                    for filter_list in right_filter:
                        filter_list.append(new_right_filter)
        if isinstance(index_bounds, bool):
            if len(left_filter) == 1 and len(splited_index) == 1:
                return search_query.get_all(*left_filter[0], index=selected_index)
            return search_query.get_all(*left_filter, index=selected_index)
        if len(left_filter) > 1:
            raise QueryBuildException("Cannot use multiply index with between statement, please rewrite query or write query via rethinkdb")
        if len(left_filter[0]) == 1:
            # Just base unpack, to fix privous initial pack
            left_filter = left_filter[0]
            right_filter = right_filter[0]
        # Fix bound to not have None value
        default_bound_value = False
        if isin_used:
            if index_bounds[0] is False or index_bounds[1] is False:
                raise QueryBuildException("Cannot build valid query with one_of and between, please rewrite query or write query via rethinkdb")
            default_bound_value = True
        left_bound, right_bound = cls.wrap_bounds(index_bounds, default_bound_value)
        return search_query.between(
            left_filter[0], right_filter[0], index=selected_index,
            left_bound=left_bound, right_bound=right_bound
        )

    @classmethod
    def process_simple_statement(cls, search_query: R.RqlQuery, statement: QueryStatement) -> R.RqlQuery:
        row = R.row[statement.left.row_name]
        if statement.statement_type == StatementType.isin:
            rethinkdb_expr = R.expr(statement.right)
            return search_query.filter(lambda doc: rethinkdb_expr.contains(doc[statement.left.row_name]))
        if statement.statement_type == StatementType.bound:
            interval: Interval = statement.right
            if interval.left_close and interval.right_close:
                return search_query.filter((row >= interval.left_bound) & (row <= interval.right_bound))
            if interval.left_close and not interval.right_close:
                return search_query.filter((row >= interval.left_bound) & (row < interval.right_bound))
            if not interval.left_close and interval.right_close:
                return search_query.filter((row > interval.left_bound) & (row <= interval.right_bound))
            if not interval.left_close and not interval.right_close:
                return search_query.filter((row > interval.left_bound) & (row < interval.right_bound))
        return search_query.filter(getattr(row, f'__{statement.statement_type.name}__')(statement.right))

    @classmethod
    def process_complicated_statement(cls, search_query: R.RqlQuery, statement: QueryStatement) -> R.RqlQuery:
        if statement.statement_type == StatementType.isin:
            return search_query.filter(lambda doc: doc[statement.right.row_name].contains(doc[statement.left.row_name]))
        if statement.statement_type == StatementType.bound:
            raise QueryBuildException("How did you even get here?")
        return search_query.filter(getattr(R.row[statement.left], f'__{statement.statement_type.name}__')(statement.right))

    @classmethod
    def process_not_indexes_statements(
            cls, search_query: R.RqlQuery, simple_fields: List[str],
            statement_dict: Dict[str, QueryStatement]) -> R.RqlQuery:
        for simple_field in simple_fields:
            statement = statement_dict.get(simple_field, None)
            if statement:
                if statement.complicated:
                    search_query = cls.process_complicated_statement(search_query, statement)
                else:
                    search_query = cls.process_simple_statement(search_query, statement)
        return search_query

    @classmethod
    @overload
    def build_query(cls, model_class, query: QueryStatement) -> R.RqlQuery:
        pass

    @classmethod
    @overload
    def build_query(cls, model_class, query: EmptyQueryStatement) -> R.RqlQuery:  # pylint: disable=function-redefined
        pass

    @classmethod
    @overload
    def build_query(cls, model_class, query: QueryStatementsCollection) -> R.RqlQuery:  # pylint: disable=function-redefined
        pass

    @classmethod
    def build_query(cls, model_class, query) -> R.RqlQuery:  # pylint: disable=function-redefined
        if isinstance(query, EmptyQueryStatement):
            return R.table(model_class._table).filter(lambda doc: False)
        if isinstance(query, QueryStatement):
            new_query = QueryStatementsCollection()
            new_query.add_statement(query)
            query = new_query
        search_query = R.table(model_class._table)
        statement_dict = query.keyword_statements
        secondary_indexes = []
        simple_fields = []
        for field_name in statement_dict.keys():
            if field_name in model_class._fields and model_class._fields.get(field_name).secondary_index:
                secondary_indexes.append(field_name)
            else:
                simple_fields.append(field_name)
        if secondary_indexes:
            selected_index, unused_fields = model_class.get_index_policy().select_secondary_index(secondary_indexes)
            if unused_fields:
                simple_fields.extend(unused_fields)
            search_query = cls.secondary_indexes_query(search_query, selected_index, query.keyword_statements)
        search_query = cls.process_not_indexes_statements(search_query, simple_fields, statement_dict)
        return search_query
