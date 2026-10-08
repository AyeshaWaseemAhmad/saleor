from typing import Any

from ...account.models import Group, User, UserManager
from ...permission.enums import get_permissions
from ..models import CustomerType


def get_or_create_default_customer_type() -> CustomerType:
    customer_type, _ = CustomerType.objects.get_or_create(
        is_default=True,
        defaults={"name": "Default", "slug": "default"},
    )
    return customer_type


def dangerously_get_or_create_superuser(
    email: str, password: str | None = None, **extra_fields: Any
) -> tuple[User, bool]:
    """Create a superuser for unittests with the given email and password.

    This should never be called for production use (due to lack of
    validation).
    """
    if user := User.objects.filter(email=email).first():
        return user, False
    user = dangerously_create_test_user(
        email=email, password=password, is_staff=True, is_superuser=True, **extra_fields
    )
    group, group_created = Group.objects.get_or_create(name="Full Access")
    if group_created:
        group.permissions.add(*get_permissions())
    group.user_set.add(user)
    return user, True


def dangerously_create_test_user(
    email, password=None, is_staff=False, is_active=True, **extra_fields
):
    """Create a user for unittests with the given email and password.

    This should never be called for production use (due to lack of
    validation).
    """
    email = UserManager.normalize_email(email)
    extra_fields.pop("username", None)

    if "customer_type" not in extra_fields and "customer_type_id" not in extra_fields:
        extra_fields["customer_type"] = get_or_create_default_customer_type()

    user = User(email=email, is_active=is_active, is_staff=is_staff, **extra_fields)
    if password:
        user.set_password(  # nosemgrep: python.django.security.audit.unvalidated-password.unvalidated-password
            password
        )
    user.save()
    return user
