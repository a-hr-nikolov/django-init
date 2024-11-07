import pytest

from apps.utils.text import slugify_unique


@pytest.fixture
def mock_db_model():
    pass


@pytest.fixture
def mock_model_class():
    """Fixture for a mock model class."""

    class MockQuerySet:
        def values_list(self, field_name, flat):
            return []

    class MockManager:
        def filter(self, *args, **kwargs):
            return MockQuerySet()

    class MockModel:
        _default_manager = MockManager()

    return MockModel


def test_slugify_unique_no_conflict(mock_model_class):
    unique_slug = slugify_unique(mock_model_class, "New Slug")
    assert unique_slug == "new-slug"


def test_slugify_unique_with_conflicts(mock_model_class):
    def mock_filter(**kwargs):
        class MockQuerySet:
            def values_list(self, field_name, flat):
                return [
                    "example-slug",
                    "example-slug-1",
                    "example-slug-2",
                ]  # Existing slugs

        return MockQuerySet()

    mock_model_class._default_manager.filter = mock_filter

    # Test with conflicting slugs
    unique_slug = slugify_unique(mock_model_class, "Example Slug")
    assert unique_slug == "example-slug-3"


def test_slugify_unique_with_custom_field(mock_model_class):
    def mock_filter(**kwargs):
        class MockQuerySet:
            def values_list(self, field_name, flat):
                return ["custom-slug", "custom-slug-1"]

        return MockQuerySet()

    mock_model_class._default_manager.filter = mock_filter

    # Test with custom slug field
    unique_slug = slugify_unique(
        mock_model_class, "Custom Slug", slug_field="custom_field"
    )
    assert unique_slug == "custom-slug-2"
