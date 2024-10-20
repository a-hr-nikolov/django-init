import pytest
from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.users.models import BaseUser
from apps.users.services import user_create


class UserCreateTests(TestCase):
    def test_user_without_password_is_created_with_unusable_one(self):
        user = user_create(email="random_user@hacksoft.io")

        self.assertFalse(user.has_usable_password())

    def test_user_with_capitalized_email_cannot_be_created(self):
        user_create(email="random_user@hacksoft.io")

        with self.assertRaises(ValidationError):
            user_create(email="RANDOM_user@hacksoft.io")

        self.assertEqual(1, BaseUser.objects.count())


@pytest.mark.django_db
def test_user_without_password_is_created_with_unusable_one():
    user = user_create(email="random_user@hacksoft.io")

    assert not user.has_usable_password()
