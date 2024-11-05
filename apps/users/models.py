import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager as BUM
from django.db import models

from apps.common.models import BaseModel

# Taken from here:
# https://docs.djangoproject.com/en/stable/topics/auth/customizing/#a-full-example
# With some modifications

# Also take a look at:
# https://simpleisbetterthancomplex.com/article/2021/07/08/what-you-should-know-about-the-django-user-model.html


class BaseUserManager[T: "BaseUser"](BUM):
    def create_user(self, email, is_active=True, is_admin=False, password=None) -> T:
        if not email:
            raise ValueError("Users must have an email address")

        user: T = self.model(
            email=self.normalize_email(email.lower()),
            is_active=is_active,
            is_admin=is_admin,
        )

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None) -> T:
        user = self.create_user(
            email=email,
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # This should potentially be an encrypted field
    jwt_key = models.UUIDField(default=uuid.uuid4)

    # ==================================================================================
    #
    # PROFILE FIELDS
    #
    # ==================================================================================
    # This can potentially be extracted into a UserProfile model with a OneToOneField.
    # ==================================================================================
    # first_name = models.CharField(max_length=255, null=True, blank=True)
    # last_name = models.CharField(max_length=255, null=True, blank=True)
    # ...

    # ==================================================================================
    # MODEL CONFIG
    # ==================================================================================
    objects: BaseUserManager = BaseUserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def is_staff(self):
        return self.is_admin
