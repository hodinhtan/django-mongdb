# from pymemcache.client import base
# client = base.Client(("localhost", 11211))

# client.set('tan', 'huh')

# c = client.get('tan')

# print(c)
from django.test import TestCase, override_settings

class TestMemcached(TestCase):
    assert True