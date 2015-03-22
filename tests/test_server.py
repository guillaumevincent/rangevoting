import unittest

from repository import MockRepository
from server import Server


class ServerTestCase(unittest.TestCase):
    def setUp(self):
        self.repository = MockRepository()

    def test_server_respond_200_ok_on_index(self):
        server = Server(self.repository)
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()
        self.assertEqual(200, self.app.get('/').status_code)

    def test_server_register_handlers(self):
        server = Server(self.repository)
        self.assertGreater(len(server.bus.handlers), 0)

    def test_register_handler_has_repository(self):
        server = Server(self.repository)
        handler = next(iter(server.bus.handlers.values()))
        self.assertIsNotNone(handler.repository)