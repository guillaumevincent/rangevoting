import json
import unittest

from repository import MockRepository
from server import Server


class SpyBus():
    def __init__(self):
        self.last_command = None

    def send(self, command):
        self.last_command = command


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
                                 data=json.dumps({'question': 'test question ?', 'choices': ['c1', 'c2', 'c3']}),
                                 content_type='application/json')
        self.assertEqual(201, response.status_code)

    def test_command_is_properly_created(self):
        server = Server(self.repository)
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()
        server.bus = SpyBus()
        self.app.post('/rangevotes/',
                      data=json.dumps({'question': 'test question ?', 'choices': ['c1', 'c2', 'c3']}),
                      content_type='application/json')

        self.assertEqual('test question ?', server.bus.last_command.question)
        self.assertEqual(['c1', 'c2', 'c3'], server.bus.last_command.choices)