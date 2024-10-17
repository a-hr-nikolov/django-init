# Django Init

A Django starter setup for quick project configuration. Inspired by [HackSoft's Django Styleguide Example](https://github.com/HackSoftware/Django-Styleguide-Example).

For initial information on the style, check [HackSoft's Django Styleguide](https://github.com/HackSoftware/Django-Styleguide).

Below I will only comment on things I've changed or have a different philosophy on.

## GenericAPIView and subclasses

HackSoft is generally against generic API classes, because they handle a lot of things through serializers, and maybe a bit of magic. I largely agree, but I think they are fine for read-only APIs. It could be argued that maintaining two different approaches for read and write APIs is a bad convention, but I don't think why it would be. Using generic classes gives you more convenient pagination options, and you still know what is going on under the hood. Even HackSoft specifies that the base GenericAPIView is fine for using. Adding a few mixins on top seems fine to me.

## Filtering

This follows from the previous point. HackSoft argue that filtering should be done on selectors. Again, to me this depends largely on our needs. If we have very complex filtering requirements, then sure. But in many circumstances we can have filtering within the API. This works well with generic views, because they allow some conveniences by default. Many times isolating the filtering to a service/selector layer only adds an abstraction that does literally nothing, aside from existing for its own sake. We may argue it enhances testability, and to me that is the only valid argument.
