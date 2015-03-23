import unittest

from repository import MockRepository
from server import Server


class ServerTestCase(unittest.TestCase):
    def setUp(self):
        self.repository = MockRepository()

    def test_server_register_handlers(self):
        server = Server(self.repository)
        self.assertGreater(len(server.bus.handlers), 0)

    def test_register_handler_has_repository(self):
        server = Server(self.repository)
        handler = next(iter(server.bus.handlers.values()))
        self.assertIsNotNone(handler.repository)

    def test_create_command_respond_201_created(self):
        server = Server(self.repository)
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()
        response = self.app.post('/rangevotes/',
                                 data={'question': 'question test', 'choices': 'c1, c2, c3'},
                                 headers={'content-type': 'application/json'})
        self.assertEqual(201, response.status_code)
