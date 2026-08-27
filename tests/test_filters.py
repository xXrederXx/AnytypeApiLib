import pytest

from AnyApi import Filter, FilterGroup


def test_nested_expression_builds_openapi_shape():
    filters = FilterGroup.or_(
        FilterGroup.and_(
            Filter("status").select().eq("done"),
            Filter("priority").select().eq("high"),
        ),
        Filter("created_date").date().gt("2026-01-01"),
    )

    assert filters.build() == {
        "operator": "or",
        "conditions": [
            {
                "property_key": "created_date",
                "condition": "gt",
                "date": "2026-01-01",
            },
        ],
        "filters": [
            {
                "operator": "and",
                "conditions": [
                    {"property_key": "status", "condition": "eq", "select": "done"},
                    {"property_key": "priority", "condition": "eq", "select": "high"},
                ],
                "filters": [],
            },
        ],
    }


@pytest.mark.parametrize(
    ("builder", "field", "value"),
    [
        ("text", "text", "hello"),
        ("number", "number", 42.5),
        ("select", "select", "done-id"),
        ("multi_select", "multi_select", ["one", "two"]),
        ("date", "date", "2026-01-01"),
        ("checkbox", "checkbox", True),
        ("files", "files", ["file-id"]),
        ("url", "url", "https://example.com"),
        ("email", "email", "user@example.com"),
        ("phone", "phone", "+49123456789"),
        ("objects", "objects", ["object-id"]),
    ],
)
def test_each_filter_format_uses_openapi_value_field(builder, field, value):
    condition = getattr(Filter("property"), builder)().eq(value)

    assert condition.build() == {
        "property_key": "property",
        "condition": "eq",
        field: value,
    }


@pytest.mark.parametrize(
    "condition",
    ["eq", "ne", "gt", "gte", "lt", "lte", "contains", "ncontains", "in", "nin", "all"],
)
def test_all_value_conditions_serialize(condition):
    filter_builder = Filter("name").text()
    value = "one"

    method = "in_" if condition == "in" else condition
    assert getattr(filter_builder, method)(value).build() == {
        "property_key": "name",
        "condition": condition,
        "text": value,
    }


def test_empty_conditions_have_no_value_field():
    assert Filter("description").empty().build() == {
        "property_key": "description",
        "condition": "empty",
    }
    assert Filter("description").nempty().build() == {
        "property_key": "description",
        "condition": "nempty",
    }


def test_groups_support_multiple_conditions_and_nested_groups():
    filters = FilterGroup.and_(
        Filter("name").text().contains("project"),
        Filter("done").checkbox().eq(False),
        FilterGroup.or_(Filter("kind").select().eq("task"), Filter("kind").select().eq("page")),
    )

    assert filters.build() == {
        "operator": "and",
        "conditions": [
            {"property_key": "name", "condition": "contains", "text": "project"},
            {"property_key": "done", "condition": "eq", "checkbox": False},
        ],
        "filters": [
            {
                "operator": "or",
                "conditions": [
                    {"property_key": "kind", "condition": "eq", "select": "task"},
                    {"property_key": "kind", "condition": "eq", "select": "page"},
                ],
                "filters": [],
            },
        ],
    }


@pytest.mark.parametrize(
    ("builder", "value"),
    [("number", "42"), ("checkbox", "true"), ("text", 42), ("select", None)],
)
def test_invalid_scalar_values_are_rejected(builder, value):
    with pytest.raises(TypeError):
        getattr(Filter("property"), builder)().eq(value)


def test_invalid_array_values_are_rejected():
    with pytest.raises(TypeError):
        Filter("tags").multi_select().all("tag")

    with pytest.raises(TypeError):
        Filter("tags").multi_select().all(["tag", 3])


def test_value_free_conditions_are_only_available_on_direct_filter():
    with pytest.raises(AttributeError):
        Filter("name").text().empty("ignored")


def test_invalid_group_items_are_rejected():
    with pytest.raises(TypeError):
        FilterGroup.and_("not a filter")


def test_property_key_must_be_non_empty():
    with pytest.raises(ValueError):
        Filter("")