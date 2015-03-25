import uuid
import json
import unittest

from bus import Result

from server import Server
from repository import MockRepository


class SpyBus():
    def __init__(self):
        self.last_command = None

    def send(self, command):
        self.last_command = command
        return Result()


class ServerTestCase(unittest.TestCase):
    def setUp(self):
        self.repository = MockRepository()
        self.server = Server(self.repository)
        self.server.app.config['TESTING'] = True
        self.app = self.server.app.test_client()

    def test_server_register_handlers(self):
        self.assertGreater(len(self.server.bus.handlers), 0)

    def test_register_handler_has_repository(self):
        handler = next(iter(self.server.bus.handlers.values()))

        self.assertIsNotNone(handler.repository)

    def test_create_rangevotes_respond_201_created(self):
        response = self.app.post('/rangevotes/',
                                 data=json.dumps({'question': 'test question ?', 'choices': ['c1', 'c2', 'c3']}),
                                 content_type='application/json')

        self.assertEqual(201, response.status_code)

    def test_create_bad_rangevotes_respond_400_bad_request(self):
        response = self.app.post('/rangevotes/',
                                 data=json.dumps({'question': '', 'choices': []}),
                                 content_type='application/json')

        self.assertEqual(400, response.status_code)

    def test_command_is_properly_created(self):
        self.server.bus = SpyBus()

        self.app.post('/rangevotes/',
                      data=json.dumps({'question': 'test question ?', 'choices': ['c1', 'c2', 'c3']}),
                      content_type='application/json')

        self.assertEqual(type(uuid.uuid4()), type(self.server.bus.last_command.uuid))
        self.assertEqual('test question ?', self.server.bus.last_command.question)
        self.assertEqual(['c1', 'c2', 'c3'], self.server.bus.last_command.choices)

    def test_return_uuid_of_rangevote(self):
        self.server.bus = SpyBus()

        response = self.app.post('/rangevotes/',
                                 data=json.dumps({'question': 'test question ?', 'choices': ['c1', 'c2', 'c3']}),
                                 content_type='application/json')
        location = '/rangevotes/' + str(self.server.bus.last_command.uuid)

        self.assertTrue(location in response.headers['Location'])