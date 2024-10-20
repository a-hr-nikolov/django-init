import django_filters
from django.db.models.query import QuerySet

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
