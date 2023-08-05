"""
Tests for the sprockets.clients.memcached package

"""
import mock
import os
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from sprockets.clients import memcached


class TestGetServers(unittest.TestCase):

    def tearDown(self):
        for key in ['MEMCACHED_SERVERS', 'TEST1_MEMCACHED_SERVERS']:
            if key in os.environ:
                del os.environ[key]

    def test_get_servers_for_prefixed_key(self):
        os.environ['TEST1_MEMCACHED_SERVERS'] = '1.1.1.1:11211,1.1.1.2:11211'
        self.assertListEqual(memcached._get_servers('TEST1'),
                             ['1.1.1.1:11211', '1.1.1.2:11211'])

    def test_get_servers_for_non_prefixed_key(self):
        os.environ['MEMCACHED_SERVERS'] = '2.1.1.1:11211'
        self.assertListEqual(memcached._get_servers(None), ['2.1.1.1:11211'])

    def test_get_servers_returns_default_value(self):
        self.assertListEqual(memcached._get_servers(None), ['127.0.0.1:11211'])


class TestClientWrapsMemcacheClient(unittest.TestCase):

    @mock.patch('memcache.Client.__init__')
    def test_client_super_init(self, mock_init):
        memcached.Client()
        mock_init.assert_called_once_with(['127.0.0.1:11211'])


class ClientIntegrationTests(unittest.TestCase):

    def setUp(self):
        self.client = memcached.Client()
        self.client.incr('test')
        if any([s.deaduntil for s in self.client.servers]):
            raise unittest.SkipTest('No memcached daemon present')

    def test_that_incr_returns_a_value_for_a_set_key(self):
        self.client.set('test-incr', 2)
        self.assertEqual(self.client.incr('test-incr'), 3)

    def test_that_set_key_is_gettable(self):
        self.client.set('foo', 'bar', 60)
        self.assertEqual(self.client.get('foo'), 'bar')
