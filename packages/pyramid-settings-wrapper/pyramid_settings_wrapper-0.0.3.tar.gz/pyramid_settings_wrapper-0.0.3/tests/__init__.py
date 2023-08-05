import unittest
from functools import partial
from pyramid.paster import get_config_loader
import pyramid_settings_wrapper

class TestWrapper(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pyramid_config = get_config_loader('tests/testing.ini').get_settings('app:main')
        # Make an extensible conf object with only config data passed in
        cls.partconf = partial(pyramid_settings_wrapper.Settings, cls.pyramid_config)

    def test_config_strip_prefix(self):
        """Test prefix stripping works."""
        conf = self.partconf(prefix=['test'])
        self.assertTrue(isinstance(conf.string, str))
        self.assertEqual(conf.string, "test")
        self.assertFalse(hasattr(conf, 'pyramid_unrelated'))

    def test_config_strip_sub_prefix(self):
        """Test multiple prefix stripping works."""
        conf = self.partconf(prefix=['test', 'subsection'])
        self.assertTrue(isinstance(conf.string, str))
        self.assertEqual(conf.string, "subsection")
        # There is no test.subsection.boolean attr
        self.assertFalse(hasattr(conf, 'boolean'))

    def test_config_dot_replace(self):
        conf = self.partconf(dot_replace="CAT")
        """Test that dots in attribute names are replaced."""
        self.assertTrue(isinstance(conf.testCATstring, str))
        self.assertEqual(conf.testCATstring, "test")

    def test_config_defaults(self):
        """Test that defaults are loaded."""
        defaults = {'new_string': {'val': 'new_string'}}
        conf = self.partconf(defaults=defaults, prefix=['test'])
        self.assertEqual(conf.new_string, 'new_string')

    def test_config_defaults_override(self):
        """Test that defaults are overridden by config."""
        defaults = {'float': {'val': 'ice-cream'}}
        conf = self.partconf(defaults=defaults, prefix=['test'])
        self.assertEqual(float(conf.float), 3.141592654)

    def test_config_default_keys_only(self):
        defaults = {'string': {'val': 'test'}}
        with self.assertLogs() as log_handler:
            conf = self.partconf(defaults=defaults, default_keys_only=True, prefix=['test'])
            self.assertTrue(any(log.levelname == "WARNING" for log in log_handler.records))

    def test_config_string_class_asbool(self):
        """Check that asbool() works correctly."""
        conf = self.partconf(prefix=['test'])
        self.assertTrue(conf.boolean.asbool())
        # Implicit __bool__ call
        self.assertTrue(conf.boolean)

    def test_config_string_class_aslist(self):
        """Check that aslist() parses strings to lists."""
        test_list = ['cat', 'dog', 'fish']
        conf = self.partconf(prefix=['test'])
        self.assertIsInstance(conf.list.aslist(), list)
        self.assertListEqual(conf.list.aslist(), test_list)

    def test_sphinx_doc(self):
        """sphinx docs should contain default settings."""
        conf = self.partconf(prefix=['test'], defaults={'string': {'val': 'string', 'desc': 'string description'}})
        docs = conf.sphinx_doc()
        self.assertTrue('string description' in docs)


if __name__ == "__main__":
    unittest.main()
