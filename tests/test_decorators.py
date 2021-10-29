import unittest
from gehu.context import check_config


class tests_decorators(unittest.TestCase):

    def setUp(self) -> None:
        self.config = {
            'username': None,
            'password': None,
        }

    def test_config_exists(self):
        """tests results if config exists"""
        def func(x): return x
        self.assertIsInstance(check_config(func), str)
