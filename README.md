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

## Selectors, generic views, and filters

Selectors are HackSoft's name for query services. They are a way to follow the uniform access principle, but... I don't like HackSoft's implementation. For example, I don't agree with their decision to put the query-param filtering logic on selectors. It leads to indirection, not to mention that user-specified filters are not a concern of the model itself (or the service layer). This can easily be solved in a much more straight-forward manner with `filter_backends`, `filterset_fields`, `search_fields`, and `ordering_fields`.

There are two arguments against those:

1. They require QuerySet access.
2. They do not explicitly validate the query parameters.

The first argument is valid only if you don't think QuerySets should be exposed. But I don't see that as a problem, as you'll see in a second. The second argument has a bit more ground, but actually, the filter backends do in fact take care of validation (at least a basic one). And if we need some more serious query param validation, we can always define a query param serializer and a filterset class that uses it. It's really a non-issue.

Does that mean that selectors are pointless? Not really. They are a great way to handle access logic, i.e. providing a pre-filtered QuerySet, which is transparent to the API. In fact, what I call "a selector" is a very simple permission filtering abstraction over what could simply be a [model manager](#the-model-manager-alternative). We can have that manager completely closed by default (i.e. have its `get_queryset` method return `queryset.none()`), and only providing a

Anyway, here are my guidelines.

### Return QuerySets

Selectors should only ever return querysets, not lists or single values. That way we can utilize GenericAPIView, ListAPIView and RetrieveAPIView at least for READ operations and pagination convenience. We can also use the querysets for further chaining, if necessary (e.g. some `.values()` calls, annotations, etc.)

There are two general ways to use them for generic views: either in the `get_queryset` method as a return value for it, or directly within a request handler method. For example, `get_object_or_404` takes a model, a queryset, or a manager. Since we shouldn't ever touch the model directly, this is where we pass our filtered queryset selector.

### Expect the requesting user

Selectors should usually (if not always) require the requesting user (which can be AnonymousUser). They will use that to "secure" the request by having it pass through an authorization (permission) filter function (an example can be seen in the next section). Then we can sprinkle some additional details. For example, say we have a resource we want to list, but don't want to have its contents available until some condition is met (e.g. a digital product may be listed, but its contents shouldn't be available). We can easily return some info in a detail view, but have it redacted by our selector (e.g. through an annotation that overrides a field and another one that may specify the restricted status).

Since the return value will always be a queryset, if there are some API-specific filters we want, we can go ahead and apply them. For example, a specific endpoint may need to return 404 for a restricted resource, which would otherwise return details with redacted content.

### Why this pattern?

1. It separates permissions from user-requested filtering.
2. It works with plain and generic API views.
3. It can be separately tested.
4. It can still utilize permission_classes simply as authentication checks
5. It gives us a lot of flexibility with the endpoints.

### Example

#### Selectors

```python
def _publication_filter_user_visible(
    req_user: BaseUser | AnonymousUser,
) -> QuerySet[Publication]:
    if req_user.is_staff:
        return Publication.objects.get_queryset()

    base_condition = Q(publish_date__lte=timezone.now())

    if not req_user.is_authenticated:
        return Publication.objects.filter(base_condition)

    is_owner = Q(owner__pk=req_user.pk)
    # add more permissions here, ex.:
    # is_manager = Q(owner__managers_pk=req_user.pk)
    full_condition = base_condition | is_owner

    return Publication.objects.filter(full_condition)


def publication_get_list_queryset(
    requested_by: BaseUser | AnonymousUser,
) -> QuerySet[Publication]:
    qs = _publication_filter_user_visible(requested_by)
    return qs


def publication_get_detail_queryset(
    requested_by: BaseUser | AnonymousUser,
) -> QuerySet[Publication]:
    qs = _publication_filter_user_visible(requested_by)
    # qs = qs.annotate(body=Case(When(not_purchased, then=""), restricted=Case(...)))
    return qs
```

### The model manager alternative

If you don't fancy the selector, and prefer to work via a model manager, there a few things you need to do.

1. Override the `get_queryset` method to return `super().get_queryset().none()`. That way the manager will always return empty querysets if used directly.
2. Define a private method for permission filtering.
3. Define another method (e.g. `get_allowed_queryset(user)`), which will return the permission-filtered queryset.
4. Add any additional QuerySet suppliers. For example, I prefer to have list and detail view queryset methods, even if they are initially the same.
5. On the model first define a standard manager (e.g. `manager = models.Manager()`), and only then override the `objects`. That way you wouldn't have to configure the meta class with an appropriate default manager (i.e. with a regular queryset),

```python
class PublicationManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().none()

    def get_allowed_list_queryset(self, user: BaseUser | AnonymousUser) -> models.QuerySet["Publication"]:
        ...

    def get_allowed_detail_queryset(self, user: BaseUser | AnonymousUser) -> models.QuerySet["Publication"]:
        ...

    def _publication_filter_user_visible(
        req_user: BaseUser | AnonymousUser,
    ) -> QuerySet[Publication]:
        if req_user.is_staff:
            return Publication.objects.get_queryset()

        base_condition = Q(publish_date__lte=timezone.now())

        if not req_user.is_authenticated:
            return Publication.objects.filter(base_condition)

        is_owner = Q(owner__pk=req_user.pk)
        # add more permissions here, ex.:
        # is_manager = Q(owner__managers_pk=req_user.pk)
        full_condition = base_condition | is_owner

        return Publication.objects.filter(full_condition)


class Publication(BaseModel):
    ...
    manager = models.Manager()
    objects = PublicationManager()
    ...
```

## A note on API endpoints

My API endpoint approach differs significantly from HackSoft's. They have an endpoint for every single action. However, due to Django and DRF's limitations, this leads to a very bad REST implementation. Here is what I mean:

```
   GET  /resources              -- list view request
  POST  /resources/create       -- create view request
   GET  /resources/<pk>         -- detail view request
   PUT  /resources/<pk>/update  -- update view request
DELETE  /resources/<pk>/delete  -- delete view request (can possible be in another endpoint)
```

This isn't such a big deal, but it is not very RESTful, and complicates the URLconf. You should really only have 2 general endpoints per resource - `/resources` and `/resources/<pk>`, i.e. list and detail endpoints. If you really need to define separate views for those, there are actually routing hacks (i.e. define the method on one view, but delegate it to another). However, I have yet to find a situation where I cannot make the generic endpoints work. For example, if I need separate permission classes, I simply override `get_permission_classes`. This applies to pretty much everything.

### My approach

1. Use ListAPIView for getting a resource list (`get` method) and creating a resource (`post` method).
2. Use RetrieveAPIView for getting a resource's details (`get` method), updating a resource (`put` method) and deleting a resource (`delete` method).
3. Have separate input and output serializers. Set the `serializer_class` attribute to the output serializer, because in most cases the `get` method will be auto-implemented.
4. Define `permission_classes` with DRF syntax (using `&` and `|` for combining permissions) for authentication permissions.

### Example

```python
class PublicationListActionsAPI(generics.ListAPIView):
    # ==================================================================================
    # LIST
    # ==================================================================================
    class ListSerializer(serializers.Serializer):
        pk = serializers.IntegerField(read_only=True)
        owner: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(
            read_only=True
        )
        owner_name = serializers.SerializerMethodField(read_only=True)
        title = serializers.CharField()
        body = serializers.CharField(write_only=True)
        slug = serializers.CharField(required=False)
        publish_date = serializers.DateTimeField(required=False)
        created_at = serializers.DateTimeField(read_only=True)
        updated_at = serializers.DateTimeField(read_only=True)
        behind_paywall = serializers.BooleanField(read_only=True)

        def get_owner_name(self, obj: Publication) -> str:
            return obj.owner.full_name()

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ListSerializer
    search_fields = ["title"]
    filterset_fields = ["owner", "behind_paywall"]

    def get_queryset(self) -> QuerySet[Publication]:
        return publication_get_list_queryset(self.request.user)

    # ==================================================================================
    # CREATE
    # ==================================================================================
    class CreateSerializer(serializers.Serializer):
        title = serializers.CharField()
        body = serializers.CharField()
        slug = serializers.CharField(required=False)
        publish_date = serializers.DateTimeField(required=False)

    def post(self, request: Request) -> Response:
        serializer = self.CreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if TYPE_CHECKING:
            assert isinstance(request.user, BaseUser)

        publication_create(owner=request.user, **serializer.validated_data)

        return Response(status=status.HTTP_201_CREATED)


class PublicationDetailActionsAPI(generics.RetrieveAPIView):
    # ==================================================================================
    # GET
    # ==================================================================================
    class OutputSerializer(serializers.Serializer):
        pk = serializers.IntegerField()
        owner: serializers.PrimaryKeyRelatedField = serializers.PrimaryKeyRelatedField(
            read_only=True
        )
        owner_name = serializers.SerializerMethodField()
        title = serializers.CharField()
        body = serializers.CharField()
        slug = serializers.CharField()
        publish_date = serializers.DateTimeField()
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()
        behind_paywall = serializers.BooleanField()

        def get_owner_name(self, obj: Publication) -> str:
            return obj.owner.full_name()

    permission_classes = [
        permissions.IsAdminUser | IsManager | (IsReadOnly & IsFreeOrHasPaid)
    ]
    serializer_class = OutputSerializer

    def get_queryset(self) -> QuerySet[Publication]:
        qs = publication_get_detail_queryset(self.request.user)

        return qs

    # ==================================================================================
    # UPDATE
    # ==================================================================================
    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(required=False)
        body = serializers.CharField(required=False)
        slug = serializers.CharField(required=False)
        publish_date = serializers.DateTimeField(required=False)

    def put(self, request: Request, pk: int) -> Response:
        qs = self.get_queryset()
        obj = get_object_or_404(qs, pk=pk)
        self.check_object_permissions(request, obj)

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        publication_update(publication=obj, **serializer.validated_data)

        return Response(status=status.HTTP_200_OK)

    # ==================================================================================
    # DELETE
    # ==================================================================================
    def delete(self, request: Request, pk: int) -> Response:
        qs = self.get_queryset()
        obj = get_object_or_404(qs, pk=pk)
        self.check_object_permissions(request, obj)

        publication_delete(publication=obj)

        return Response(status=status.HTTP_204_NO_CONTENT)
```
