pyramid_settings_wrapper
========================

This module takes a pyramid `config.registry.settings` config object and transforms it into a class.

Features
--------

* Takes a (optional) `defaults` configuration dictionary, overridden by values in the ini-file.

* Optionally reject config options not in defaults to start with. (`default_keys_only`)

* Build sphinx documentation of config options from the resulting class.

* Access config as either class attributes, or via `__dict__`

* Attributes have `asbool()` and `aslist()` methods added (based on `pyramid.settings` methods).
  `__bool__` == `asbool` so attributes can be tested for truthyness.

* Select only config options with a specific list of `prefix` parts - stripping the prefix when creating attributes.

* `.` in attribute names will be replaced with `dot_replace` (defaults to `_`)


Example
--------

Supposing you have a Pyramid ini-file containing:

```
[app:main]
use = egg:my_app
sqlalchemy.url = sqlite://

my_app.name = Joe
my_app.admin = true
my_app.groups = admin,finance,office
my_app.nosuchitem = trees
```

Your app `__init__.py` contains:

```
from pyramid.config import Configurator
import pyramid_settings_wrapper

defaults = {
    'name': {'val': '', 'desc': 'User's name'},
    'admin': {'val': False, 'desc': 'Is this user an administrator?'},
    'groups': 'val': []},
}

def main(global_config, **settings):
    config = Configurator(settings=settings)
    settings = pyramid_settings_wrapper.Settings(config.registry.settings, defaults=defaults, default_keys_only=True, prefix=['my_app'])

    # Logged warning: "Invalid configuration options: {'nosuchitem': 'trees'}

    # Access as attribute
    print(settings.name)  # 'Joe'

    # Test truthyness
    if settings.admin:
        print("Is an admin")

    # Access as list
    print([group for group in settings.groups.aslist()])  # ['admin', 'finance', 'office']

    # Get all config options
    settings.__dict__
```
