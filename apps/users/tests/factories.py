import factory

from apps.users.models import BaseUser
from apps.utils.faker import get_faker

faker = get_faker()


class UserFactory(factory.django.DjangoModelFactory):
    email = faker.unique.email(safe=True)
    is_admin = False

    class Meta:
        model = BaseUser

    @classmethod
    def _create(cls, model_class, email, is_admin, *args, **kwargs) -> BaseUser:
        user = BaseUser.objects.filter(email=email).first()
        if user:
            return user
        return BaseUser.objects.create_user(
            email=email, is_admin=is_admin, password="dummy-pass"
        )

    @classmethod
    def default(cls) -> BaseUser:
        return cls.create(email="john_doe_johnson_unique@example.com")
