# Django Init

A Django starter setup for quick project configuration. Inspired by [HackSoft's Django Styleguide Example](https://github.com/HackSoftware/Django-Styleguide-Example).

For initial information on the style, check [HackSoft's Django Styleguide](https://github.com/HackSoftware/Django-Styleguide).

## The Short Version

I've made some changes to HackSoft's "cookie-cutter" project above. Below is the summary. At some point I'd like to create my own [cookie-cutter](https://github.com/cookiecutter/cookiecutter-django) properly, this one is basically a manual implementation of that.

### More explanation

HackSoft's guide is targeted towards people with at least basic knowledge of Django and Python packages. I try not to assume that, so I explain why something is included and how exactly. If you don't see an explanation, that's because I am not actively using a package, and it's there for someone else's convenience. Or I haven't yet had the time to update this README.

### More in-project documentation

Some configs require touching multiple files, which makes it challenging to track them. Wherever relevant I have added docstrings, detailing where related configuration can be found.

### Type annotation updates

Certain places did not have type annotations or they were of older styles, which may be fine, but I don't like how it plays with the IDE and additional imports. So I've added or improved type annotations wherever relevant.

### Introduced `uv`

I'm using **[uv](https://docs.astral.sh/uv/)** for virtual environment and dependency management. I believe this is the future for Python, and it is almost entirely `pip` and `pip-tools` compatible. It is also simply better than `poetry`, which this project utilized before `uv`. If you are not familiar with the tool, check [Virtual Environments and Dependency Management](#virtual-environments-and-dependency-management).

### Modularity

I've tried to comment out any dependency that may not be needed in a project. That way any third-party integration is opt-in, rather than opt-out.

I've decided to configure the following things:

- Django REST Framework
- pytest (and pytest-django)
- CORS
- mypy (for basic usage)

You can freely delete anything else that isn't needed in your project. That would mostly be the files in `config.settings`. Check [Non-Django Configuration](#non-django-configuration) for more information.

---

## The Long Version

### Virtual Environments and Dependency Management

This project uses **[uv](https://docs.astral.sh/uv/getting-started/)** for its venv and dependency management through a `pyproject.toml` file in the root directory. It handles everything in one place, provides a `.lock` file and is generally much nicer to use than either `poetry` or regular `pip`. It is actually compatible with `pip`, and uses a standard `pyproject.toml` file, unlike `poetry`.

[Install `uv`](https://docs.astral.sh/uv/getting-started/installation/#installation-methods) according to your system's needs. I prefer using `pipx`, but that is a separate tool that also has to be installed, if you don't have it. Unlike Python-based tools, `uv` can work great as a global install, because it isn't actually Python-dependent. It can actually manage Python versions for you.

### General Configuration

Configuration is split between `config`, `config.django`, and `config.settings`.

The most notable thing in `/config/` is `env.py`. It is for loading environment variables, and also includes a couple of shared resources (common both to `config.django` and `config.settings`).

`config.django` holds only Django-specific settings (ref. [Where is `settings.py`?](#where-is-settingspy)).

`config.settings` holds most non-Django third-party package configuration.

#### Where is `settings.py`?

This module does not exist. Instead, the configuration is now found at `config.django.base`, which is extended by `config.django.production`, and `config.django.test` in the same directory. It has been correctly configured in `manage.py` for local development.

I have additionally improved the layout with clear separation between the different configuration blocks. Before that they were only a single commented line, very hard to scan. Be sure to make comments noticeable in your IDE, as some themes configure them with very low contrast.

If your base config grows large, configuration blocks can be further split into modules (e.g. dj-database.py, dj-static.py, dj-drf.py, etc.).

**Example Config Block Comment**

```python
########################################################################################
#
# DATABASE
#
########################################################################################
# https://docs.djangoproject.com/en/stable/ref/settings/#databases
########################################################################################
```

### Django REST Framework

All files that have to do with DRF specific configuration and usage are in the **apps/api** directory. The `REST_FRAMEWORK` option is found in `config.django.base`.

All API endpoints are located within their specific app directory. They **are not** placed within the `apps/api` directory. This is because we want an app to be as self-contained as possible, without having to trace how the data flows through it by jumping between apps (at least not as much).

Since DRF allows for a lot of configuration (auth, permissions, pagination, etc.), the `REST_FRAMEWORK` option is configured with sensible defaults. Alternatives may be commented, but not every alternative will be available.

#### Exceptions in DRF

DRF has an issue. Its philosophy of validating through serializers clashes with the idea that validation should happen on the model layer. This [serializer vs model validation](https://github.com/encode/django-rest-framework/discussions/7850) problem will likely never get solved... by DRF. But we can do it ourselves!

The gist of it is that DRF uses its own `ValidationError`, which doesn't map to Django's `ValidationError`. On top of that, DRF isn't uniform it how it handles its own validation messages. HackSoft has an interesting proposal, but if doesn't suit you, you can use the simpler exception handler in `apps.api.exception_handler`. It maps Django exceptions to DRF exceptions to promote model-level validation.

My advice is to use HackSoft's error handling suggestion, as it provides a really nice and uniform error messaging. Just make sure that whatever custom errors you define all inherit from `ApplicationError` as defined in `common.exceptions`.

**NOTE:** HackSoft's approach defines the business-specific exceptions in `core.exceptions`. I've opted to place them in the `common` app.

### Non-Django Configuration

All third-party integrations are handled through their respective modules in `config.settings`. Then they are imported at the end of `config.django.base`.

**IMPORTANT:** Most third-party configuration imports are commented out. Don't forget to uncomment them if you are going to use them.

---

# Personal Style Guide

## Services vs Fat Models

If you've been in the Django world for a while, you may be familiar with the clash between HackSoft's proposed service layer, and James Bennett's fat models. Read his opinion [here](https://www.b-list.org/weblog/2020/mar/16/no-service/) and [here](https://www.b-list.org/weblog/2020/mar/23/still-no-service/).

A lot of what is said makes sense, and you would think that a core Django developer would probably be right. Well... The thing is that other core Django developers (or DRF developers) have different opinions. Look for them if you want, but some are for service layers, others are for encapsulated fat models. Other folks also have [interesting takes](https://news.ycombinator.com/item?id=27607337).

Technically speaking, I err on the side of services, though using the model layer directly for READ-ONLY operations is fine to me in many situations. James Bennett says that services basically create our project specific ORM. I agree, but that's actually the point. However, our ORM is simple, uniform, intuitive... and safe.

For example, accessing a model's .save() method, or updating fields directly on a model instance should be a no-go in a view. But... Django doesn't stop that. I can argue it encourages it by having validation and creation logic handled via forms (and serializers).

So what do we end up doing? I've read recommendations that creation and updating should only be done via specific manager and model methods, never by directly assigning model fields, or using the model constructor. So, you are telling me that... we are writing a service method, instead of a service function? Who cares whether you call `User.objects.create()` vs `user_create()`, or `user_instance.update(...)` vs `user_update(...)`? In fact, the service approach has many benefits - it allows for cross-cutting concerns within the function, it provides better IDE autocomplete, and it is a layer of safety so that you don't go thinking "I will do this here just once, and maybe fix it later".

I also really dislike the argument that "service function with cross-cutting concerns are doing too much". Yes, and? Stop the "clean code" worshipping, and start being pragmatic. Yes, the functions may be creating an instance of this and that, sending a message, queuing a task, and saving the object. Is this too much? Yeah. Can it be solved reasonably? Not really, unless you want to really complicate your system. Sometimes that is necessary. Often it isn't. Just let functions do a lot, when they need to, and it is clear what is going on. Stop following rules for the sake of following rules.

## Selectors, GenericAPIView, and who should be filtering stuff?

Aside from services, HackSoft also introduced the idea of selectors (or query services). I am not entirely sure how I feel about them, as often they are simply a pass-through to QuerySets and Managers. But then... they are a way to follow the uniform access principle.

The problem comes when we decide what to do about filtering. There are two approaches - handle it in the selectors, or handle it in the API. The latter is especially convenient if you use generic API classes. Is this an issue though?

HackSoft is generally against generic API classes, because they handle a lot of things through serializers, and maybe a bit of magic. I largely agree for WRITE APIs, but I think they are _mostly_ fine for read-only APIs. It could be argued that maintaining two different approaches for READ and WRITE APIs is a bad convention. However, I believe it can actually reinforce the idea that READ and WRITE are fundamentally different operations that do not benefit from uniform approaches.

Furthermore, using generic classes give you more convenient pagination options, and you still know what is going on under the hood. Even HackSoft specifies that the base GenericAPIView is fine. I'd go as far as saying that **ReadOnlyModelViewSet** is fine too.

Back to selectors and filtering - what should we do with them? I say let the generic API handle it through automatic filtering. If it makes you feel better, use a pass-through selector in the `get_queryset` method, instead of directly operating with the QuerySet.

### My reasoning

1. Automatic API filtering is by definition simple. It doesn't require a lot of setup, aside from configuring the **filter_backends** property and related fields.
2. You are rather configuring, not writing query code, so no API-to-backend communication convention is being broken.
3. If the setup seems finicky, it means more complex filtering is needed. No need to fight the generic API view, instead use a selector.
4. Following from the above, we can infer the following:
   - Selectors should exist as a part of the **service layer**, so their API is available (and discoverable) in the IDE.
   - If they exist for a certain model, that means filtering is more complex for said model. If they don't exist, we can assume filtering is simple.
   - A new person will more quickly realize which APIs are tied to more complex backend interactions, and which - to simpler ones.

So for the price of not having uniform filtering logic on every single API (though it would be the uniform for most), we get the benefits of understanding the complexity of an API backend, without having to look at it specifically.

I am adapting this argument from [James Bennett's article on properties](https://www.b-list.org/weblog/2023/dec/21/dont-use-python-property/). In our Django project hiding the filtering for the sake of uniformity may actually be withholding information that should rather be obvious.

### But testability is better with a selector layer!

Fair enough. But what will we be testing? If a selector only exists for uniformity reasons, tests just make sure that we are not screwing up the passthrough. This is still important, and a good safety net in case we need to complicate the filtering later. However, it doesn't really prove we're correctly configuring the API to use the filtering.

At the end of the day, there has to be an integration test, which checks whether an API call gets the expected results. We may have written the perfect filter, but if we are not correctly configuring the API, it wouldn't matter.

This gives us 2 options:

1. Write a selector, write tests for it, and always use it (for uniformity reasons). Write API integration tests nevertheless.
2. Postpone writing the selector, until it is needed. Write API integration tests nevertheless.

To me the second options seems preferable, as we won't be optimizing prematurely. But I also understand why someone would want the uniformity. Do what feels better.
