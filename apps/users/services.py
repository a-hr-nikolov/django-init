import django_filters
from django.db import transaction
from django.db.models.query import QuerySet

from apps.common.services import model_update
from apps.users.models import BaseUser


class BaseUserFilter(django_filters.FilterSet):
    class Meta:
        model = BaseUser
        fields = ("id", "email", "is_admin")


def user_get_login_data(*, user: BaseUser):
    return {
        "id": user.id,
        "email": user.email,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "is_superuser": user.is_superuser,
    }


def user_list(*, filters=None) -> QuerySet[BaseUser]:
    filters = filters or {}

    qs = BaseUser.objects.all()

    return BaseUserFilter(filters, qs).qs


def user_create(
    *,
    email: str,
    is_active: bool = True,
    is_admin: bool = False,
    password: str | None = None,
) -> BaseUser:
    user = BaseUser.objects.create_user(
        email=email, is_active=is_active, is_admin=is_admin, password=password
    )

    return user


@transaction.atomic
def user_update(*, user: BaseUser, data) -> BaseUser:
    non_side_effect_fields = ["first_name", "last_name"]

    user, has_updated = model_update(
        instance=user, fields=non_side_effect_fields, data=data
    )

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...

    return user
