import pytest

from ...models import CustomerType
from ..utils import get_or_create_default_customer_type

__all__ = [
    "customer_type",
    "customer_type_with_attributes",
    "default_customer_type",
    "get_or_create_default_customer_type",
]


@pytest.fixture
def customer_type(db):
    return CustomerType.objects.create(name="B2B", slug="b2b")


@pytest.fixture
def customer_type_with_attributes(
    customer_type,
    loyalty_customer_attribute,
    description_customer_attribute,
    hidden_customer_attribute,
):
    customer_type.customer_attributes.add(
        loyalty_customer_attribute,
        description_customer_attribute,
        hidden_customer_attribute,
    )
    return customer_type


@pytest.fixture(autouse=True)
def default_customer_type(db):
    return get_or_create_default_customer_type()
