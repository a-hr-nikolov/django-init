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

### Introduced `poetry`

I'm using **poetry** for virtual environment and dependency management. If you are not familiar with the tool, check [Virtual Environments and Dependency Management](#virtual-environments-and-dependency-management).

### Modularity

I've tried to comment out any dependency that may not be needed in a project. That way any third-party integration is opt-in, rather than opt-out.

I've decided to configure the following things:

- Django REST Framework
- pytest (and pytest-django)
- CORS configured out of the box
- mypy configured out of the box (for basic usage)

You can freely delete anything else that isn't needed in your project. That would mostly be the files in `/config/settings/`. Check [Non-Django Configuration](#non-django-configuration) for more information.

## Virtual Environments and Dependency Management

### Using `Poetry`

This project uses **[poetry](https://python-poetry.org/docs/basic-usage/)** for its venv and dependency management through a [pyproject.toml](https://python-poetry.org/docs/pyproject/) file in the root directory. It handles everything in one place, provides a `.lock` file and is generally much nicer to use. Some people have reported issues using it with `Docker`, but it simply requires a bit of configuration. Read more [here](https://gist.github.com/soof-golan/6ebb97a792ccd87816c0bda1e6e8b8c2) and [here](https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0). You can also [watch this](https://www.youtube.com/watch?v=hXYFS2pOEH8).

[Install **poetry**](https://python-poetry.org/docs/#installation) according to your system's needs. You can install it in a separate venv, or globally. I prefer using `pipx`, but that is a separate tool that also has to be installed, if you don't have it.

By default `poetry` operates in [package management mode](https://python-poetry.org/docs/basic-usage/#operating-modes) and expects a directory with the package name (defined in `pyproject.toml`), but `-` (dash) is replaced with `_` (underscore). This default expectation can be changed, if we explicitly specify `tool.poetry.packages`. Read more about it [here](https://python-poetry.org/docs/pyproject/#packages). Currently, the `config` and `apps` packages have to be specified in a `packages` array.

**Basic usage**

```bash
poetry install  # installs the project, and is run after pyproject.toml changes
poetry add <name-of-dependency>  # adds packages https://python-poetry.org/docs/cli/#add
poetry add --group dev <dep>  # adds a dependency to a group named `dev`
poetry remove <dependency>
poetry update
```

**On the server**

```bash
poetry install --without dev  # list all other dependency groups to exclude
poetry install --only main  # an alternative to the previous command
```

### Using `venv` and `pip`

**NOTE:** You can use `poetry export` to export the requirements.txt file. So I strongly advise you to install **poetry** at least for that, as well as the **poetry-plugin-export**. Installation is system dependent, so I can't guide you here, but it can save a lot of work.

You are free to use the vastly inferior setup with `venv` and `pip`, but you will have to create your own `requirements.txt` file, and place it somewhere. I recommend having a `/requirements/` directory with 2 files: `base.txt` and `local.txt`, which includes `-r base.txt` as its first line (as `pip` is going to run it as a script).

```bash
python -m venv <env-name, usually .venv>

# Linux & Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

# Using poetry to generate `requirements.txt`
# The non-poetry commands below are for Linux. I don't know PowerShell, so Windows users
# are on their own here.
mkdir requirements
poetry export -f requirements.txt --output ./requirements/base.txt --without-hashes --without dev
poetry export -f requirements.txt --output ./requirements/local.txt --without-hashes --only dev
(echo "-r base.txt" && cat ./requirements/local.txt) > temp_file && mv temp_file ./requirements/local.txt

# Requirements install
pip install -r ./requirements/local.txt
```

## General Configuration

Configuration is split between `config`, `config.django`, and `config.settings`.

The most notable thing in `/config/` is `env.py`. It is for loading environment variables, and also includes a couple of shared resources (common both to `config.django` and `config.settings`).

`config.django` holds only Django-specific settings (ref. [Where is `settings.py`?](#where-is-settingspy)).

`config.settings` holds most non-Django third-party package configuration.

## Where is `settings.py`?

This module does not exist. Instead, the configuration is now found at `config.django.base`, which is extended by `config.django.production`, and `config.django.test` in the same directory. It has been correctly configured in `manage.py` for local development.

I have additionally improved the layout with clear separation between the different configuration blocks. Before that they were only a single commented line, very hard to scan. I strongly advice you to make comments noticeable in your IDE, as some themes deliberately make them almost fade into the background.

Configuration blocks can be further split into modules (e.g. dj-database.py, dj-static.py, dj-drf.py, etc.). If your base config grows large, consider splitting.

**Example Config Block Comment**

```python
########################################################################################
#
# DATABASE
#
########################################################################################
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
########################################################################################
```

## Non-Django Configuration

All third-party integrations are handled through their respective modules in `config.settings`. Then they are imported at the end of `config.django.base`.

**IMPORTANT:** Most third-party configuration imports are commented. Don't forget to uncomment them if you are going to use them.

**Currently Configured Modules:**

- CORS (with django-cors-headers)

## Django Configuration

### Django REST Framework

All files that have to do with DRF specific configuration and usage are in the **apps/api** directory. The **REST_FRAMEWORK** option is found in **config/django/base.py**.

All API endpoints are located within their specific app directory. They **are not** placed within the apps/api directory. This is because we want an app to be self-contained as much as possible, without having to trace how the data flows through it by jumping between apps (at least not as much).

Since DRF allows for a lot of configuration (auth, permissions, pagination, etc.), it is available on the **REST_FRAMEWORK** option with sensible defaults already set up. Alternatives may be commented, but not every alternative will be available.

#### Exceptions in DRF

DRF is bad at handling validation exceptions, because its philosophy of validating through serializers clashes with the idea that actual model validation should happen on the model layer. [Serializer vs model validation ](https://github.com/encode/django-rest-framework/discussions/7850)is an old problem with DRF, that will probably never be resolved.

The gist of it is that DRF uses its own ValidationError, which doesn't map to Django's ValidationError. On top of that, DRF isn't uniform it how it handles its own validation messages. HackSoft has an interesting proposal, but if doesn't suit you, you can use the simpler exception handler in **apps/api/exception_handler.py**. It maps Django exceptions to DRF exceptions to promote model-level validation.

HackSoft's approach defines the business-specific exceptions in a **core** app. In this project, I've opted to place them in a **common** app. It doesn't really matter, I just don't like **core** as to me it signals logic that is core to the project, but in reality, it isn't really core, just common.

**General Advice**: Use HackSoft's suggestion, as it provides a really nice and uniform error messaging. Just make sure that whatever custom errors you define all inherit from ApplicationError.

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
