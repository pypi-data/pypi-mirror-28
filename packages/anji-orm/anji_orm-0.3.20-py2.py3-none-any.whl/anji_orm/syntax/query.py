from abc import ABC, abstractmethod
from enum import Enum
import logging
from typing import overload, List, Dict

from ..utils import prettify_value

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.3.20"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = [
    'QueryRow', 'QueryStatement', 'StatementType', 'QueryStatementsCollection', 'Interval',
    'EmptyQueryStatement'
]

_log = logging.getLogger(__name__)


class Interval:

    __slots__ = ['left_bound', 'right_bound', 'left_close', 'right_close']

    def __init__(
            self, left_bound, right_bound,
            left_close: bool = False, right_close: bool = False) -> None:
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.left_close = left_close
        self.right_close = right_close

    def contains_interval(self, other: 'Interval') -> bool:
        if self.left_bound > other.left_bound:
            return False
        if self.left_bound == other.left_bound and other.left_close and not self.left_close:
            return False
        if self.right_bound < other.right_bound:
            return False
        if self.right_bound == other.right_bound and other.right_close and not self.right_close:
            return False
        return True

    def clone(self) -> 'Interval':
        return Interval(
            self.left_bound,
            self.right_bound,
            left_close=self.left_close,
            right_close=self.right_close
        )

    @property
    def valid(self):
        if self.left_bound < self.right_bound:
            return True
        return self.left_bound == self.right_bound and self.left_close and self.right_close

    def __eq__(self, other) -> bool:
        if not isinstance(other, Interval):
            return False
        return self.left_bound == other.left_bound and self.right_bound == other.right_bound and self.left_close == other.left_close and self.right_close == other.right_close

    def __contains__(self, item) -> bool:
        return (
            ((self.left_bound < item) or (self.left_close and self.left_bound == item))
            and
            ((self.right_bound > item) or (self.right_close and self.right_bound == item))
        )

    def __str__(self) -> str:
        return f"{'[' if self.left_close else '('}{self.left_bound}, {self.right_bound}{']' if self.right_close else ')'}"


class StatementType(Enum):

    eq = '=='  # pylint: disable=invalid-name
    lt = '<'  # pylint: disable=invalid-name
    gt = '>'  # pylint: disable=invalid-name
    ne = '!='  # pylint: disable=invalid-name
    le = '<='  # pylint: disable=invalid-name
    ge = '>='  # pylint: disable=invalid-name
    isin = 'in'  # pylint: disable=invalid-name
    bound = 'bound'  # pylint: disable=invalid-name


class QueryStatementsCollection:

    __slots__ = ['keyword_statements', 'complicated_statements']

    def __init__(self) -> None:
        self.keyword_statements: Dict[str, 'QueryStatement'] = {}
        self.complicated_statements: List['QueryStatement'] = []

    @property
    def complicated(self) -> bool:
        return bool(self.complicated_statements)

    def add_statement(self, *statements: 'QueryStatement') -> bool:
        for statement in statements:
            if statement.complicated:
                self.complicated_statements.append(statement)
            else:
                current_statement = self.keyword_statements.get(statement.left.row_name, None)
                if current_statement is not None:
                    merged_statements: QueryStatement = current_statement & statement
                    self.keyword_statements[statement.left.row_name] = merged_statements
                    if isinstance(merged_statements, EmptyQueryStatement):
                        return False
                else:
                    self.keyword_statements[statement.left.row_name] = statement
        return True

    @overload
    def __and__(self, other: 'QueryStatement') -> 'QueryStatementsCollection':  # pylint: disable=function-redefined
        pass  # pragma: no cover

    @overload
    def __and__(self, other: 'QueryStatement') -> 'QueryStatement':  # pylint: disable=function-redefined
        pass  # pragma: no cover

    @overload
    def __and__(self, other: 'QueryStatementsCollection') -> 'QueryStatementsCollection':  # pylint: disable=function-redefined
        pass  # pragma: no cover

    def __and__(self, other):  # pylint: disable=function-redefined
        if isinstance(other, QueryStatementsCollection):
            if not self.add_statement(*other.joined_statements):
                return EmptyQueryStatement()
        else:
            if not self.add_statement(other):
                return EmptyQueryStatement()
        return self

    def __eq__(self, other) -> bool:
        if not isinstance(other, QueryStatementsCollection):
            return False
        return self.complicated_statements == other.complicated_statements and self.keyword_statements == other.keyword_statements

    def __str__(self) -> str:
        base_string = " & ".join(map(str, self.keyword_statements.values()))
        if self.complicated_statements:
            base_string += " & ".join(map(str, self.complicated_statements))
        return base_string

    def __repr__(self) -> str:
        return str(self)


class QueryStatement(ABC):

    __slots__ = ['left', 'right']

    _statement_type: StatementType = None

    def __init__(self, left, right) -> None:
        self.left = prettify_value(left)
        self.right = prettify_value(right)

    @property
    def statement_type(self) -> StatementType:
        return self._statement_type

    @staticmethod
    def _compare_leaf(leaf, other_leaf) -> bool:
        if hasattr(leaf, 'is_same'):
            if not leaf.is_same(other_leaf):
                return False
        else:
            if leaf != other_leaf:
                return False
        return True

    @overload
    def __and__(self, other: 'QueryStatement') -> 'QueryStatement':
        pass  # pragma: no cover

    @overload
    def __and__(self, other: 'QueryStatement') -> QueryStatementsCollection:  # pylint: disable=function-redefined
        pass  # pragma: no cover

    def __and__(self, other):  # pylint: disable=function-redefined
        if not self.complicated and not other.complicated and self.left.row_name == other.left.row_name:
            return self._similar_merge(other)
        collection = QueryStatementsCollection()
        collection.add_statement(self)
        collection.add_statement(other)
        return collection

    @abstractmethod
    def _similar_merge(self, other: 'QueryStatement') -> 'QueryStatement':
        """
        Abstract method that allow merge statements like connected with `and` keyword.
        Make sure, that you use merge method only for simple query statements.

        To avoid code duplicating we use next implementation matrix:
        1. eq and ne with everything
        2. bound with everythin except eq and ne
        3. isin with le, ge, gt, lt, isin
        4. le with ge, gt, lt, le
        5. lt with ge and gt, lt
        6. ge with gt, ge
        6. gt with gt
        """

    def __eq__(self, other) -> bool:
        if not isinstance(other, QueryStatement):
            return False
        if self.statement_type != other.statement_type:
            return False
        if not self._compare_leaf(self.left, other.left):
            return False
        if not self._compare_leaf(self.right, other.right):
            return False
        return True

    @property
    def complicated(self) -> bool:
        """
        Check if query statement has QueryRow on both leafs
        """
        return isinstance(self.right, type(self.left))

    def __str__(self) -> str:
        return f"{self.left} {self.statement_type.value} {self.right}"

    def __repr__(self) -> str:
        return str(self)


class EmptyQueryStatement(QueryStatement):
    """
    Empty query statement, return on incompatable statements merge
    """

    __slots__: List[str] = []

    def __init__(self) -> None:  # pylint: disable=super-init-not-called
        pass

    def __and__(self, other):
        return self

    def __eq__(self, other) -> bool:
        return isinstance(other, EmptyQueryStatement)

    @property
    def complicated(self) -> bool:
        return False

    def _similar_merge(self, other: 'QueryStatement') -> 'QueryStatement':
        return self


class QueryEqualStatement(QueryStatement):

    _statement_type = StatementType.eq

    def _similar_merge(self, other: QueryStatement) -> QueryStatement:
        compitability_check = (
            (other.statement_type == StatementType.eq and other.right == self.right)
            or
            (other.statement_type in [StatementType.isin, StatementType.bound] and self.right in other.right)
            or
            (other.statement_type == StatementType.lt and self.right < other.right)
            or
            (other.statement_type == StatementType.le and self.right <= other.right)
            or
            (other.statement_type == StatementType.ge and self.right >= other.right)
            or
            (other.statement_type == StatementType.gt and self.right > other.right)
            or
            (other.statement_type == StatementType.ne and self.right != other.right)
        )
        if compitability_check:
            return self
        return EmptyQueryStatement()


class QueryGreaterOrEqualStatement(QueryStatement):

    _statement_type = StatementType.ge

    def _similar_merge(self, other: QueryStatement) -> QueryStatement:
        if other.statement_type not in [StatementType.ge, StatementType.gt]:
            return other._similar_merge(self)
        if self.right > other.right:
            return self
        return other


class QueryGreaterStatement(QueryStatement):

    _statement_type = StatementType.gt

    def _similar_merge(self, other: QueryStatement) -> QueryStatement:
        if other.statement_type != StatementType.gt:
            return other._similar_merge(self)
        if self.right > other.right:
            return self
        return other


class QueryLowerOrEqualStatement(QueryStatement):

    _statement_type = StatementType.le

    def _similar_merge(self, other: QueryStatement) -> QueryStatement:
        if other.statement_type in [
                StatementType.eq, StatementType.ne,
                StatementType.bound, StatementType.isin]:
            return other._similar_merge(self)
        if other.statement_type in [StatementType.le, StatementType.lt]:
            if self.right < other.right:
                return self
            return other
        if self.right < other.right:
            return EmptyQueryStatement()
        return QueryBoundStatement(
            self.left,
            Interval(
                other.right, self.right,
                left_close=other.statement_type == StatementType.ge, right_close=True
            )
        )


class QueryLowerStatement(QueryStatement):

    _statement_type = StatementType.lt

    def _similar_merge(self, other: QueryStatement) -> QueryStatement:
        if other.statement_type in [
                StatementType.eq, StatementType.ne,
                StatementType.bound, StatementType.isin,
                StatementType.le]:
            return other._similar_merge(self)
        if other.statement_type == StatementType.lt:
            if self.right < other.right:
                return self
            return other
        if self.right < other.right:
            return EmptyQueryStatement()
        return QueryBoundStatement(
            self.left,
            Interval(
                other.right, self.right,
                left_close=other.statement_type == StatementType.ge, right_close=False
            )
        )


class QueryNotEqualStatement(QueryStatement):

    _statement_type = StatementType.ne

    def _similar_merge(self, other: QueryStatement) -> QueryStatement:
        compitability_check = (
            (other.statement_type == StatementType.eq and other.right == self.right)
            or
            (other.statement_type in [StatementType.isin, StatementType.bound] and self.right in other.right)
            or
            (other.statement_type == StatementType.lt and self.right < other.right)
            or
            (other.statement_type == StatementType.le and self.right <= other.right)
            or
            (other.statement_type == StatementType.ge and self.right >= other.right)
            or
            (other.statement_type == StatementType.gt and self.right > other.right)
            or
            (other.statement_type == StatementType.ne and self.right != other.right)
        )
        if not compitability_check:
            return other
        elif other.statement_type == StatementType.isin:
            new_elements = tuple(x for x in other.right if x != self.right)
            if new_elements:
                return QueryContainsStatement(self.left, new_elements)
        elif other.statement_type == StatementType.bound:
            if self.right in other.right:
                _log.warning("Currently, bound statement cannot be merged with ne statement, so just ingore ne statement")
            return other
        return EmptyQueryStatement()


class QueryContainsStatement(QueryStatement):

    _statement_type = StatementType.isin

    def _similar_merge(self, other: QueryStatement) -> QueryStatement:
        if other.statement_type in [StatementType.eq, StatementType.ne, StatementType.bound]:
            return other._similar_merge(self)
        if other.statement_type == StatementType.isin:
            intersection = tuple(x for x in self.right if x in other.right)
            if intersection:
                return QueryContainsStatement(self.left, intersection)
            return EmptyQueryStatement()
        method_name = f"__{other.statement_type.name}__"
        for element in self.right:
            if not getattr(element, method_name)(other.right):
                return EmptyQueryStatement()
        return self


class QueryBoundStatement(QueryStatement):

    _statement_type = StatementType.bound

    def _similar_merge(self, other: QueryStatement) -> QueryStatement:
        if other.statement_type in [StatementType.eq, StatementType.ne]:
            return other._similar_merge(self)
        if other.statement_type == StatementType.isin:
            for element in other.right:
                if element not in self.right:
                    return EmptyQueryStatement()
            return other
        interval = self.right.clone()
        # Convert to QueryBoundStatement to make same codebase for many statement type
        # If you want to change it, make sure that all types covered
        if other.statement_type in [StatementType.le, StatementType.lt]:
            interval.right_close = other.statement_type == StatementType.le
            interval.right_bound = other.right
            other = QueryBoundStatement(self.left, interval)
        if other.statement_type in [StatementType.ge, StatementType.gt]:
            interval.left_close = other.statement_type == StatementType.ge
            interval.left_bound = other.right
            other = QueryBoundStatement(self.left, interval)
        if other.statement_type == StatementType.bound:
            interval = other.right
        if interval.valid:
            if self.right.contains_interval(interval):
                return other
            if interval.contains_interval(self.right):
                return self
        return EmptyQueryStatement()


class QueryRow:

    __slots__ = ['row_name']

    def __init__(self, row_name: str) -> None:
        self.row_name = row_name

    def one_of(self, *variants) -> QueryStatement:
        return QueryContainsStatement(self, variants)

    def contains(self, another_row: 'QueryRow') -> QueryStatement:
        return QueryContainsStatement(another_row, self)

    def is_same(self, other) -> bool:
        if not isinstance(other, QueryRow):
            return False
        return self.row_name == other.row_name

    def __eq__(self, other) -> QueryStatement:  # type: ignore
        return QueryEqualStatement(self, other)

    def __ge__(self, other) -> QueryStatement:
        return QueryGreaterOrEqualStatement(self, other)

    def __gt__(self, other) -> QueryStatement:
        return QueryGreaterStatement(self, other)

    def __ne__(self, other) -> QueryStatement:  # type: ignore
        return QueryNotEqualStatement(self, other)

    def __lt__(self, other) -> QueryStatement:
        return QueryLowerStatement(self, other)

    def __le__(self, other) -> QueryStatement:
        return QueryLowerOrEqualStatement(self, other)

    def __str__(self) -> str:
        return f"row[{self.row_name}]"
