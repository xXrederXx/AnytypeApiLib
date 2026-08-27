from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from numbers import Real
from typing import Any, Callable, Sequence


class FilterCondition(str, Enum):
    EQ = "eq"
    NE = "ne"
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    CONTAINS = "contains"
    NCONTAINS = "ncontains"
    IN = "in"
    NIN = "nin"
    ALL = "all"
    EMPTY = "empty"
    NEMPTY = "nempty"


class FilterOperator(str, Enum):
    AND = "and"
    OR = "or"


_VALUE_CONDITIONS = frozenset(FilterCondition) - {
    FilterCondition.EMPTY,
    FilterCondition.NEMPTY,
}


class _Buildable:
    def build(self) -> dict[str, Any]:
        raise NotImplementedError


@dataclass(frozen=True)
class _FilterItem(_Buildable):
    property_key: str
    condition: FilterCondition
    value_name: str | None = None
    value: Any = None

    def build(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "property_key": self.property_key,
            "condition": self.condition.value,
        }
        if self.value_name is not None:
            result[self.value_name] = self.value
        return result


@dataclass(frozen=True)
class FilterExpression(_Buildable):
    operator: FilterOperator
    conditions: tuple[_FilterItem, ...] = ()
    filters: tuple[FilterExpression, ...] = ()

    def build(self, *, types: Sequence[str] | None = None, top_level=True) -> dict[str, Any]:
        expression = {
            "operator": self.operator.value,
            "conditions": [condition.build() for condition in self.conditions],
            "filters": [filter_.build(top_level=False) for filter_ in self.filters],
        }
        if top_level and types is None:
            return {"filters": expression}
        if types is None:
            return expression
        return {"filters": expression, "types": _validate_types(types)}


class _FormatFilter:
    def __init__(self, property_key: str, value_name: str, value_type: str):
        self._property_key = property_key
        self._value_name = value_name
        self._value_type = value_type

    def _condition(self, condition: FilterCondition, value: Any) -> _FilterItem:
        if condition not in _VALUE_CONDITIONS:
            raise ValueError(f"{condition.value} requires no value")
        validated = _validate_value(self._value_type, value)
        return _FilterItem(
            property_key=self._property_key,
            condition=condition,
            value_name=self._value_name,
            value=validated,
        )

    def eq(self, value: Any) -> _FilterItem:
        return self._condition(FilterCondition.EQ, value)

    def ne(self, value: Any) -> _FilterItem:
        return self._condition(FilterCondition.NE, value)

    def gt(self, value: Any) -> _FilterItem:
        return self._condition(FilterCondition.GT, value)

    def gte(self, value: Any) -> _FilterItem:
        return self._condition(FilterCondition.GTE, value)

    def lt(self, value: Any) -> _FilterItem:
        return self._condition(FilterCondition.LT, value)

    def lte(self, value: Any) -> _FilterItem:
        return self._condition(FilterCondition.LTE, value)

    def contains(self, value: Any) -> _FilterItem:
        return self._condition(FilterCondition.CONTAINS, value)

    def ncontains(self, value: Any) -> _FilterItem:
        return self._condition(FilterCondition.NCONTAINS, value)

    def in_(self, value: Any) -> _FilterItem:
        return self._condition(FilterCondition.IN, value)

    def nin(self, value: Any) -> _FilterItem:
        return self._condition(FilterCondition.NIN, value)

    def all(self, value: Any) -> _FilterItem:
        return self._condition(FilterCondition.ALL, value)


class Filter:
    def __init__(self, property_key: str):
        if not isinstance(property_key, str) or not property_key:
            raise ValueError("property_key must be a non-empty string")
        self.property_key = property_key

    def text(self) -> _FormatFilter:
        return _FormatFilter(self.property_key, "text", "str")

    def number(self) -> _FormatFilter:
        return _FormatFilter(self.property_key, "number", "number")

    def select(self) -> _FormatFilter:
        return _FormatFilter(self.property_key, "select", "str")

    def multi_select(self) -> _FormatFilter:
        return _FormatFilter(self.property_key, "multi_select", "strings")

    def date(self) -> _FormatFilter:
        return _FormatFilter(self.property_key, "date", "str")

    def checkbox(self) -> _FormatFilter:
        return _FormatFilter(self.property_key, "checkbox", "bool")

    def files(self) -> _FormatFilter:
        return _FormatFilter(self.property_key, "files", "strings")

    def url(self) -> _FormatFilter:
        return _FormatFilter(self.property_key, "url", "str")

    def email(self) -> _FormatFilter:
        return _FormatFilter(self.property_key, "email", "str")

    def phone(self) -> _FormatFilter:
        return _FormatFilter(self.property_key, "phone", "str")

    def objects(self) -> _FormatFilter:
        return _FormatFilter(self.property_key, "objects", "strings")

    def empty(self) -> _FilterItem:
        return _FilterItem(self.property_key, FilterCondition.EMPTY)

    def nempty(self) -> _FilterItem:
        return _FilterItem(self.property_key, FilterCondition.NEMPTY)

    def not_empty(self) -> _FilterItem:
        return self.nempty()


def _validate_string(value: Any) -> str:
    if not isinstance(value, str):
        raise TypeError("filter value must be a string")
    return value


def _validate_number(value: Any) -> Real:
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError("filter value must be a number")
    return value


def _validate_boolean(value: Any) -> bool:
    if not isinstance(value, bool):
        raise TypeError("filter value must be a boolean")
    return value


def _validate_strings(value: Any) -> list[str]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise TypeError("filter value must be a sequence of strings")
    if not all(isinstance(item, str) for item in value):
        raise TypeError("filter value must be a sequence of strings")
    return list(value)


def _validate_types(types: Sequence[str]) -> list[str]:
    if isinstance(types, (str, bytes)) or not isinstance(types, Sequence):
        raise TypeError("types must be a sequence of strings")
    if not all(isinstance(type_name, str) and type_name for type_name in types):
        raise TypeError("types must be a sequence of non-empty strings")
    return list(types)


_VALIDATORS: dict[str, Callable[[Any], Any]] = {
    "str": _validate_string,
    "number": _validate_number,
    "bool": _validate_boolean,
    "strings": _validate_strings,
}


def _validate_value(value_type: str, value: Any) -> Any:
    try:
        validator = _VALIDATORS[value_type]
    except KeyError as error:
        raise AssertionError(
            f"unknown filter value type: {value_type}") from error
    return validator(value)


class FilterGroup:
    @staticmethod
    def and_(*items: _FilterItem | FilterExpression) -> FilterExpression:
        return _group(FilterOperator.AND, items)

    @staticmethod
    def or_(*items: _FilterItem | FilterExpression) -> FilterExpression:
        return _group(FilterOperator.OR, items)


def _group(
    operator: FilterOperator,
    items: Sequence[_FilterItem | FilterExpression],
) -> FilterExpression:
    conditions: list[_FilterItem] = []
    filters: list[FilterExpression] = []
    for item in items:
        if isinstance(item, _FilterItem):
            conditions.append(item)
        elif isinstance(item, FilterExpression):
            filters.append(item)
        else:
            raise TypeError(
                "filter groups accept only filters and filter groups")
    return FilterExpression(operator, tuple(conditions), tuple(filters))


__all__ = ["Filter", "FilterGroup", "FilterCondition",
           "FilterOperator", "FilterExpression"]
