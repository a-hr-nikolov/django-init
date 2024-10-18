# Django Init

A Django starter setup for quick project configuration. Inspired by [HackSoft's Django Styleguide Example](https://github.com/HackSoftware/Django-Styleguide-Example).

For initial information on the style, check [HackSoft's Django Styleguide](https://github.com/HackSoftware/Django-Styleguide).

## Summary of My Changes (tl;dr)

- I've added more explanations wherever I think was relevant, including in this guide. HackSoft assume a basic knowledge of Django and Python packages. I try not to assume that, so I explain why something is included and how exactly. If I haven't explained it, it is because I am not actively using it, and is there for someone else's convenience. Or I haven't yet had the time to update this README.
- I dislike scattered configs, but that's sometimes inescapable. That's why where relevant I have added docstrings to explain to modules, detailing where related configuration can be found.
- I'm using **poetry** for virtual environment and dependency management.

You can freely delete anything that isn't needed in your project. That would mostly be the files in `/config/settings/`.

Detailed explanation follows.

## Virtual Environments and Dependency Management

### Using `Poetry`

This project uses **[poetry](https://python-poetry.org/docs/basic-usage/)** for its venv and dependency management through a [pyproject.toml](https://python-poetry.org/docs/pyproject/) file in the root directory. It handles everything in one place, provides a `.lock` file and is generally much nicer to use. Some people have reported issues in having it play nice with `Docker`. It simply requires a bit of configuration. Read more [here](https://gist.github.com/soof-golan/6ebb97a792ccd87816c0bda1e6e8b8c2) and [here](https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0). You can also [watch this](https://www.youtube.com/watch?v=hXYFS2pOEH8).

Install **poetry** globally (no guide, as it depends on your OS).

I've configured it in [dependency management mode](https://python-poetry.org/docs/basic-usage/#operating-modes) (it defaults to package management). Package management mode requires a directory with the same name as the package, but `-` is replaced with `_`. There are three general approaches when using **Django**:

1. Rename the `apps` directory to `my_poetry_project` (not recommended, will break the world).
2. Rename the `config` directory to `my_poetry_project` (the most painless). Don't forget to update manage.py (i.e. config.django.base > my_project.django.base).
3. Create a `my_poetry_project` directory, and only put an `__init__.py` file in.
4. Create a `my_poetry_project` directory, and put everything Django-related in it. Beware though, as this will break paths and you will have to set them manually. For example, in `/config/django/base.py` you will have to add a `.parent` to `BASE_URL`.

I lean towards the 2nd option, but all of them will require more distribution configuration, when you are ready to use **poetry** to package the code. Only the 4th option wouldn't really need that.

```toml
[tool.poetry]
name = ""  # ex. "my-project", requires dir "/my_project", if package-mode = true.
version = "0.1.0"
description = ""
authors = ["John Doe <john.doe@example.com>"]
readme = "README.md"
package-mode = false  # set to true to enable package mode
```

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

I will use this starter setup to also talk a little bit about the HackSoft's style guide mentioned above. I will mainly comment on things I have a different philosophy on. Keep in mind that if you are torn between my approach and theirs, default to theirs. Compared to them, my experience is miniscule.

That being said, if you are not the one deciding the style for your team (like me, for example), it doesn't really matter. I am perfectly fine working with any convention, as long as there actually is one. This here is for playground projects mostly. And while some would argue that we shouldn't worry about the structure and architecture of pet projects, I feel like developing a feel for proper structure can only happen if you focus on it. Yes, even on pet projects.

Anyway, consider everything below **a tangent** to the starter setup. It isn't needed to get coding.

## Services vs Fat Models

If you've been in the Django world for a while, you may be familiar with the clash between HackSoft's proposed service layer, and James Bennett's fat models. Read his opinion [here](https://www.b-list.org/weblog/2020/mar/16/no-service/) and [here](https://www.b-list.org/weblog/2020/mar/23/still-no-service/).

A lot of what is said makes sense, and you would think that a core Django developer would probably be right. Well... The thing is that other core Django developers (or DRF developers) have different opinions. Look for them if you want, but some are for service layers, others are for encapsulated fat models. Other folks also have [interesting takes](https://news.ycombinator.com/item?id=27607337).

This is all to say that there isn't a consensus. In my view, the middle road is best, as you will see below. But technically speaking, I err on the side of services. James Bennett says that services basically create our project specific ORM. And... yes! That's actually the point. The difference is that our ORM is safe and encapsulated, and you will find it harder to shoot yourself in the foot.

I also really dislike the argument that "service functions with cross-cutting concerns are doing too much, if they are necessary". It smells like "clean code" bs. Yes, the service functions are doing a lot. They are creating an instance of this and that, sending a message, queuing a task, and saving the object. Is this too much? Yeah. Can it be solved reasonably? Not really, unless you really go hard with signals. But that's a bad pattern in and of itself, so you better implement a pub-sub system -- maybe RabbitMQ -- and then deal with a bit more latency, more maintenance overhead, etc., etc. Just let functions do a lot, man. Sometimes they have to.

That being said, I consider ORM objects to actually be public API, and only use services when there are indeed cross-cutting concerns. I'm still torn on whether or not maintaining the access uniformity principle is worth it here. We will see.

## GenericAPIView and subclasses

HackSoft is generally against generic API classes, because they handle a lot of things through serializers, and maybe a bit of magic. I largely agree, but I think they are fine for read-only APIs.

It could be argued that maintaining two different approaches for read and write APIs is a bad convention. Fair enough. If it confuses you, ditch it. However, I believe it can actually reinforce the idea that READ and WRITE are fundamentally different operations and require a different approach.

Furthermore, using generic classes gives you more convenient pagination options, and you still know what is going on under the hood. Even HackSoft specifies that the base GenericAPIView is fine. Perhaps a **ReadOnlyModelViewSet** is going too far, perhaps not. The only "drawback" I see is that it requires a router.

## Filtering

This follows from the previous point. HackSoft argue that filtering should be done on selectors. This seems perfectly reasonable at first, until you realize those selectors are often nothing more than a pass-through abstraction over managers and querysets.

If we have very complex filtering requirements, then sure, by all means, write a selector and add filter kwargs to it. But let automatic filtering happen on the API.

### My reasoning

1. Automatic API filtering is by definition simple. It doesn't require a lot of setup, aside from configuring the **filter_backends** property and related fields.
2. You are rather configuring, not writing query code, so no API-to-backend communication convention is being broken.
3. If the setup seems finicky, it means more complex filtering is needed. No need to fight generic API view, instead just resort to writing the selector service.
4. Following from the above, we can infer the following:
   - Selectors should exist as a part of the **service layer**, so their API is available (and discoverable) in the IDE.
   - If they exist for a certain model, that means filtering is more complex for said model. If they don't exist, we can assume filtering is simple.
   - A new person will more quickly realize which APIs are tied to more complex backend interactions, and which - to simpler ones.

So for the price of not having uniform service-layer access for every single model, we get the benefits of understanding the complexity of an API backend, without having to look at it specifically.

I am adapting this argument from [James Bennett's article on properties](https://www.b-list.org/weblog/2023/dec/21/dont-use-python-property/). Writing a property for the sake of aesthetics hides information that should better be obvious. Here hiding filtering behind a "uniform" notation also seems to withhold information that should better be apparent.

### But testability is better with a selector layer!

This alone was almost enough to sway me towards having selectors. However, after some consideration with tests, I realized this is actually a moot point for many selectors.

See, what we are really doing within simple selectors is... passing everything to a queryset, really. Maybe using a django-filter. So what will we be testing? That we correctly configured a pass-through abstraction? Since it only exists for uniformity reasons, tests just make sure that we are not screwing up, not that we are writing a valuable piece of code.

In other words, not only is the selector pointless, but now we have to write tests for it just in case. That all means a pointless selector requires more code than it looks at first glance, without providing any utility.

But I hear you. It doesn't feel right to not test the filtering logic. However, what is it that we really need to test? Is it not that the API actually passes the correct parameters and gets the expected results? This is why the selector exists, right? I don't see any way around that.

Ultimately, we have to test the API. We may have written the perfect filter, but if we are not correctly configuring the API, it wouldn't matter. On the other hand, if we are testing the API, why not simply have the selection logic there? Since filtering on the API is by configuration, we can simply test whether the API returns what's expected.

Of course, for a selector that does complex filtering, we have to test it separately, so we know our filtering logic works. But then we are truly testing what brings value, not a pass-through abstraction.

All in all, simple selectors shouldn't exist, as the API test will cover the filtering. When complex selectors do exist, we need an additional test, and we still **should not** skip the API one. "But this is integration testing!", I hear you say. Call it whatever. It's what's valuable here.

### But what if we need complex filtering in the future?

Then refactor. It's not a big deal. You have the API test to cover for that, and if it isn't sufficient, it only means that you need to rework the API anyway. Or you've written a bad test.

What this question really asks is "Why not optimize for potential requirements?" This, of course, is the root of all software evils - premature optimization. Don't code for requirements you don't have. If you keep your API code simple, refactoring for potential complex filtering requirements will not be a big deal.
