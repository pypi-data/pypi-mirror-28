django-simple-activity
======================

[![PyPI](https://img.shields.io/pypi/v/django-simple-activity.svg)](https://pypi.python.org/pypi/django-simple-activity)
[![Python Versions](https://img.shields.io/pypi/pyversions/django-simple-activity.svg)](https://pypi.python.org/pypi/django-simple-activity)
[![Build Status](https://travis-ci.org/richardasaurus/django-simple-activity.png?branch=master)](https://travis-ci.org/richardasaurus/django-simple-activity)


Simple, generic, activity streams from the actions on your site.

Supports Django versions 1.10.x, 1.11.x, 2.0 and above.

## Installation

1. Install using `pip`...

    ```pip install django-simple-activity```

2. Add `'activity'` to your `INSTALLED_APPS` setting.

    ```python
    INSTALLED_APPS = (
        ...
        'activity',
    )
    ```

3. Ensure `django.contrib.contenttypes` is above `django.contrib.auth` in your installed apps ([why? read here](http://stackoverflow.com/questions/25947951/genericforeignkey-violation-only-when-user-model-given-postgres/25949737#25949737)).


## Example Usage


#### Creating Activity Actions


```python
from activity.logic import add_action, get_action_text
user = User.objects.get(username='bob')

# actor and verb example
action = add_action(actor=user, verb='joined the website!')
print(get_action_text(action)) -> 'bob joined the website!'

# actor, verb and action
another_user = User.objects.get(username='jessica')
action = add_action(
    actor=user,
    verb='made friends with',
    action=another_user,
    timestamp=timezone.now() - timedelta(days=2)
)
print(get_action_text(action)) -> 'bob made friends with jessica 2 days ago'

```
Further examples are in the [tests](https://github.com/richardasaurus/django-simple-activity/blob/master/src/tests/test_activity.py).


#### Retrieving Activity Actions

Get **all** Activity Action records:

```python
Action.objects.all()
```


Get all **public** Activity Action records:
```python
Action.objects.public()
```

Get all **private** Activity Action records, where the actor is a given user

```python
Action.objects.private(actor=user)  # user being a Django User model instance
```

Here's an example use of `django-simple-activity` which uses [django signals](https://docs.djangoproject.com/en/dev/topics/signals/)
to trigger off the creation of an activity action when a new user registers on the site.


```python
from django.db.models.signals import pre_save
from django.dispatch import receiver
from activity.logic import add_action
from . models import UserProfile


@receiver(pre_save, sender=UserProfile)
def new_user_activity(sender, **kwargs):
    profile = kwargs.get('instance')
    # if no profile.id yet, then this is a new user registering
    if not profile.id:
        add_action(actor=profile.user, verb='joined the website!')
```


## Running the unit tests

To test dependency installation and run the tests:

```
pip install tox
tox
```
