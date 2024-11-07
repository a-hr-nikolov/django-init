from itertools import count

from django.db import models
from django.utils.text import slugify


def slugify_unique(
    model_class: type[models.Model], text: str, slug_field="slug"
) -> str:
    slug = slugify(text, allow_unicode=False)
    slug_matches = model_class._default_manager.filter(
        **{f"{slug_field}__startswith": slug}
    ).values_list(slug_field, flat=True)

    num_of_matches = len(slug_matches)
    if num_of_matches < 1:
        return slug

    for i in count(num_of_matches):
        new_slug = f"{slug}-{i}"
        if new_slug not in slug_matches:
            break
    return new_slug
