# Django Init

A Django starter setup for quick project configuration. Inspired by [HackSoft's Django Styleguide Example](https://github.com/HackSoftware/Django-Styleguide-Example).

For initial information on the style, check [HackSoft's Django Styleguide](https://github.com/HackSoftware/Django-Styleguide).

## Usage

Delete anything that isn't needed in your project. That would mostly be the files in **config/settings/**.

You will not find a **settings.py** module however. Instead, that file is now **config/django/base.py**, which is extended by **production.py**, and **test.py** in the same directory. It has been correctly configured in manage.py for local development.

## Personal Style Guide

I will use this starter setup to also talk a little bit about the style guide mentioned above. I will mainly comment on things I have a different philosophy on. Keep in mind that if you are torn between my approach and theirs, default to theirs. Compared to them, my experience is miniscule. However, I think that my mind works well with abstractions (I have an intuitive "feel" for them), and my approach just "fits" better in my eyes.

That being said, if you are not the one deciding the style for your team (like me, for example), it doesn't really matter. I am perfectly fine working with whatever conventions. This here is for playground projects mostly. And while some would argue that we shouldn't worry about the structure and architecture of pet projects, I feel like developing a feel for proper structure can only happen if you focus on it. Yes, even on pet projects.

Anyway, consider everything below **a tangent** to the starter setup. It isn't needed to get coding.

### GenericAPIView and subclasses

HackSoft is generally against generic API classes, because they handle a lot of things through serializers, and maybe a bit of magic. I largely agree, but I think they are fine for read-only APIs.

It could be argued that maintaining two different approaches for read and write APIs is a bad convention. Fair enough. If it confuses you, ditch it. However, I believe it can actually reinforce the idea that READ and WRITE are fundamentally different operations and require a different approach.

Furthermore, using generic classes gives you more convenient pagination options, and you still know what is going on under the hood. Even HackSoft specifies that the base GenericAPIView is fine. Perhaps a **ReadOnlyModelViewSet** is going too far, perhaps not. The only "drawback" I see is that it requires a router.

### Filtering

This follows from the previous point. HackSoft argue that filtering should be done on selectors. This seems perfectly reasonable at first, until you realize those selectors are often nothing more than a pass-through abstraction over managers and querysets.

If we have very complex filtering requirements, then sure, by all means, write a selector and add filter kwargs to it. But let automatic filtering happen on the API.

#### My reasoning

1. Automatic API filtering is by definition simple. It doesn't require a lot of setup, aside from configuring the **filter_backends** property and related fields.
2. You are rather configuring, not writing query code, so no API-to-backend communication convention is being broken.
3. If the setup seems finicky, it means more complex filtering is needed. No need to fight generic API view, instead just resort to writing the selector service.
4. Following from the above, we can infer the following:
   - Selectors should exist as a part of the **service layer**, so their API is available (and discoverable) in the IDE.
   - If they exist for a certain model, that means filtering is more complex for said model. If they don't exist, we can assume filtering is simple.
   - A new person will more quickly realize which APIs are tied to more complex backend interactions, and which to more simple ones.

So for the price of not having uniform service-layer access for every single model, we get the benefits of understanding the complexity of an API backend, without having to look at it specifically.

I am adapting this argument from [James Bennett's article on properties](https://www.b-list.org/weblog/2023/dec/21/dont-use-python-property/). Writing a property for the sake of aesthetics hides information that should better be obvious. Here hiding filtering behind a "uniform" notation also seems to withhold information that should better be apparent.

#### But testability is better with a selector layer!

This alone was almost enough to sway me towards having selectors. However, after some consideration with tests, I realized this is actually a moot point for many selectors.

See, what we are really doing within simple selectors is... passing everything to a queryset, really. Maybe using a django-filter. So what will we be testing? That we correctly configured a pass-through abstraction? Since it only exists for uniformity reasons, tests just make sure that we are not screwing up, not that we are writing a valuable piece of code.

In other words, not only is the selector pointless, but now we have to write tests for it just in case. That all means a pointless selector requires more code than it looks at first glance, without providing any utility.

But I hear you. It doesn't feel right to not test the filtering logic. However, what is it that we really need to test? Is it not that the API actually passes the correct parameters and gets the expected results? This is why the selector exists, right? I don't see any way around that.

Ultimately, we have to test the API. This goes against HackSoft's conventions, but I don't see how this isn't the case. We may have written the perfect filter, but if we are not correctly configuring the API, it wouldn't matter. On the other hand, if we are testing the API, why not simply have the selection logic there? Since filtering on the API is by configuration, we can simply test whether the API returns what's expected.

Of course, for a selector that does complex filtering, we have to test it separately, so we know our filtering logic works. But then we are truly testing what brings value, not an arbitrary "for-the-sake-of-having-it" abstraction.

All in all, simple selectors shouldn't exist, as the API test will cover the filtering. When complex selectors do exist, we need an additional test, and we still **cannot** skip the API one.

#### But what if we need complex filtering in the future?

Then refactor. It's not a big deal. You have the API test to cover for that, and if it isn't sufficient, it only means that you need to rework the API anyway. Or you've written a bad test.

What this question really asks is "Why not optimize for potential requirements?" This, of course, is the root of all software evils - premature optimization. Don't code for requirements you don't have. If you keep your API code simple, refactoring for potential complex filtering requirements will not be a big deal.
