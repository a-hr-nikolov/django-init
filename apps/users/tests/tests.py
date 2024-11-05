import pytest
from django.core.exceptions import ValidationError

from apps.users.models import BaseUser
from apps.users.services import user_create


@pytest.fixture
def user(db) -> BaseUser:
    return user_create(email="john_doe@example.com")


def test_user_without_password_is_created_with_unusable_one(user: BaseUser):
    assert not user.has_usable_password()


@pytest.mark.django_db
def test_user_with_capitalized_email_cannot_be_created_if_uncapitalized_exists(
    user: BaseUser,
):
    email = user.email
    email_parts = email.split("@")
    email_parts[0] = email_parts[0].upper()
    email = "@".join(email_parts)
    with pytest.raises(ValidationError):
        user_create(email=email)

    assert BaseUser.objects.count() == 1
