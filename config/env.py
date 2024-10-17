import environ
from django.core.exceptions import ImproperlyConfigured

env = environ.Env()

BASE_DIR = environ.Path(__file__) - 2
APPS_DIR = BASE_DIR.path("apps")


def env_to_enum(enum_cls, value):
    """
    Used by settings to convert environment variables to defined enum types, when such
    are expected. Check **config.settings.email_sending** for an example.

    Args:
        enum_cls: An enum type, which can be matched against **value**.
        value: The actual environment variable, loaded via an environ.Env instance.

    Raises:
        django.core.exceptions.ImproperlyConfigured:
            The provided environment variable isn't found on the defined enum.
    """
    for x in enum_cls:
        if x.value == value:
            return x

    raise ImproperlyConfigured(
        f"Env value {repr(value)} could not be found in {repr(enum_cls)}"
    )
