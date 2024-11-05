import factory

from apps.users.models import BaseUser

DUMMY_EMAILS = [
    "john_doe@example.com",
    "alex_smith@example.com",
    "jane_doe@example.com",
    "mike_jones@example.com",
    "sarah_lee@example.com",
    "emma_davis@example.com",
    "david_clark@example.com",
    "lisa_white@example.com",
    "matt_johnson@example.com",
    "amy_wilson@example.com",
]

DUMMY_PASSWORD = "dummy-password"


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Iterator(DUMMY_EMAILS)
    is_admin = False
    password = DUMMY_PASSWORD

    class Meta:
        model = BaseUser
        django_get_or_create = ["email"]

    @classmethod
    def _create(cls, model_class, email, is_admin, *args, **kwargs) -> BaseUser:
        return BaseUser.objects.create_user(
            email=email, is_admin=is_admin, password=DUMMY_PASSWORD
        )


def supply_user() -> BaseUser:
    usr = BaseUser.objects.filter(email="john_doe@example.com").first()
    if usr:
        return usr
    return BaseUser.objects.create_user(email="john_doe@example.com", password="lame")
