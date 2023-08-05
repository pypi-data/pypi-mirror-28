"""pyramid_settings_wrapper module."""

# pylint:disable=line-too-long

import copy
import logging
from pyramid.settings import asbool, aslist


class ConfigString(str):
    """Add custom methods."""
    def asbool(self):
        """Access pyramid.settings.asbool in a pythonic way."""
        return asbool(self)

    def aslist(self):
        """Access pyramid.settings.aslist in a pythonic way."""
        return aslist(self, flatten=True)

    __bool__ = asbool


class Settings():
    """Class to store pyramid configuration settings (from the ini file)
    and provide easier programatic access to them.
    """

    def __init__(self, settings, defaults=None, default_keys_only=False, prefix=None, prefix_sep='.', dot_replace='_'):  # pylint:disable=too-many-arguments
        """
        Create attributes from settings, overriding defaults
        with values from pyramid config.

        Arguments:
            settings: Pyramid config.registry.settings dictionary.
            defaults: A dictionary of default settings {'name': {'val': 'value', 'desc': 'Description'}}
            default_keys_only: ignore any config options in inifile that aren't keys in 'defaults' (defaults to False)
            prefix: A list of prefix parts used to filter config options from the config.
            prefix_sep: Separator for joining prefix parts (defaults to '.')

        """
        self.pyramid_settings = settings
        self.defaults = defaults or {}
        self.default_keys_only = default_keys_only
        self.prefix = ''
        self.dot_replace = dot_replace
        if prefix:
            self.prefix = prefix_sep.join(prefix) + prefix_sep
        self.create_attrs()

    def create_attrs(self):
        """Create class attributes from settings."""

        # Extract pyramid_jsonapi config from settings, stripping prefix
        config = {k[len(self.prefix):].replace('.', self.dot_replace): v for k, v in self.pyramid_settings.items() if k.startswith(self.prefix)}
        result = {k: v['val'] for k, v in self.defaults.items()}

        if self.default_keys_only:
            # Update result with values from config if key in defaults
            for key in result:
                if key in config:
                    result[key] = config.pop(key)
            if config:
                logging.warning("Invalid configuration options ignored: %s", config)
        else:
            # Update with all config
            result.update(config)

        # Convert results dict to attrs
        for key, val in result.items():
            setattr(self, key, ConfigString(val))

    def sphinx_doc(self):
        """Generate sphinx-doc for inifile options."""

        docslist = []
        docslist.append("""
    **Configuration Options**

    These options can be overridden in the pyramid app ini-file.

    .. code-block:: python

    """)
        for key, data in sorted(self.defaults.items()):
            docslist.append("   # {}".format(data['desc']))
            docslist.append("   {}{} = {}\n".format(self.prefix, key, data['val']))
        return '\n'.join(docslist)
