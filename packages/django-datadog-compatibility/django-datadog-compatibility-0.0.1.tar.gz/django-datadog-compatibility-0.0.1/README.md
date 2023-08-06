# Django DataDog Integration

A simple DataDog Integration for Django. This app lets you set your integration
settings in and just call the compatibility wrapper functions. All
authentication is handled on your behalf.

## Quickstart

To get started, setup your DataDog Agent, then configure this app:

```bash
pip install django-datadog-compatibility
```

Configure your `settings.py` with DataDog and StatsD:

```python
DATADOG = {
  'ENABLED': True,
  'API_KEY': 'xxxx',
  'APP_KEY': 'xxxx',
}

STATSD_HOST = 'localhost'
STATSD_PORT = '12345'
```

You're now able to call DataDog functions:

```python
from django_datadog.compat import create_event, create_gauge

create_event('example.com.my_event',
             fmt_text='Sample event %s',
             priority='normal',
             text_args=(request.user.email, ),
             tags=['app:example'])

create_gauge('example.com.my_gauge', value=25)
```

And that's it!

## Contributing

We don't currently cover all of DataDog's functionality. If you'd like to
contribute, please open a Pull Request with the new function and a test case.

Add the function to `django_datadog/compat.py`

### Initializing

To setup your function, you usually want to initialize DataDog:

```python
from datadog import some_function

from django_datadog.utils import init_datadog

def my_custom_function():
    if init_datadog():
        some_function()
```
