import uuid
import json
import logging
import unittest

import bus
import server
import repository
import rangevoting


class SpyBus:
    def __init__(self):
        self.last_command = None

    def send(self, command):
        self.last_command = command
        return bus.Result()


class SpyQueryDispatcher:
    def __init__(self):
        self.last_query = None

    def execute(self, query):
        self.last_query = query
        return rangevoting.RangeVote(uuid=1, question='q?', choices=['c1', 'c2']).serialize()


class ServerTestCase(unittest.TestCase):
    def setUp(self):
        server.app.repository = repository.MockRepository()
        server.app.config['TESTING'] = True
        server.app.configure_handlers()
        self.app = server.app.test_client()

        root = logging.getLogger()
        root.setLevel(logging.CRITICAL)

    def test_server_register_handlers(self):
        self.assertGreater(len(server.app.bus.handlers), 0)

    def test_register_handler_has_repository(self):
        handler = next(iter(server.app.bus.handlers.values()))

        self.assertIsNotNone(handler.repository)

    def test_create_rangevotes_respond_201_created(self):
        response = self.app.post('/rangevotes',
                                 data=json.dumps({'question': 'test question ?', 'choices': ['c1', 'c2', 'c3']}),
                                 content_type='application/json')

        self.assertEqual(201, response.status_code)

    def test_create_bad_rangevotes_respond_400_bad_request(self):
        response = self.app.post('/rangevotes',
                                 data=json.dumps({'question': '', 'choices': []}),
                                 content_type='application/json')

        self.assertEqual(400, response.status_code)

    def test_command_is_properly_created(self):
        server.app.bus = SpyBus()

        self.app.post('/rangevotes',
                      data=json.dumps({'question': 'test question ?', 'choices': ['c1', 'c2', 'c3']}),
                      content_type='application/json')

        self.assertEqual(type(uuid.uuid4()), type(server.app.bus.last_command.uuid))
        self.assertEqual('test question ?', server.app.bus.last_command.question)
        self.assertEqual(['c1', 'c2', 'c3'], server.app.bus.last_command.choices)

    def test_return_uuid_of_rangevote(self):
        server.app.bus = SpyBus()

        response = self.app.post('/rangevotes',
                                 data=json.dumps({'question': 'test question ?', 'choices': ['c1', 'c2', 'c3']}),
                                 content_type='application/json')
        location = '/rangevotes/' + str(server.app.bus.last_command.uuid)

        self.assertTrue(location in response.headers['Location'])

    def test_get_rangevote(self):
        server.app.query_dispatcher = SpyQueryDispatcher()

        response = self.app.get('/rangevotes/375ce742-495f-4b0c-b831-3fb0dcc61b17', content_type='application/json')

        self.assertEqual(200, response.status_code)
        self.assertEqual('375ce742-495f-4b0c-b831-3fb0dcc61b17', server.app.query_dispatcher.last_query.uuid)

    def test_get_rangevote_404(self):
        response = self.app.get('/rangevotes/375ce742-495f-4b0c-b831-3fb0dcc61b17', content_type='application/json')

        self.assertEqual(404, response.status_code)

    def test_update_rangevote(self):
        server.app.bus = SpyBus()

        response = self.app.put('/rangevotes/375ce742-495f-4b0c-b831-3fb0dcc61b17',
                                data=json.dumps({'question': 'test question ?', 'choices': ['c1', 'c2', 'c3'], 'votes': []}),
                                content_type='application/json')
        self.assertEqual(200, response.status_code)
        self.assertEqual('375ce742-495f-4b0c-b831-3fb0dcc61b17', server.app.bus.last_command.uuid)
        self.assertEqual('test question ?', server.app.bus.last_command.question)
        self.assertListEqual(['c1', 'c2', 'c3'], server.app.bus.last_command.choices)

    def test_create_vote(self):
        server.app.bus = SpyBus()

        response = self.app.post('/rangevotes/375ce742-495f-4b0c-b831-3fb0dcc61b17/votes',
                                 data=json.dumps({'elector': 'Guillaume Vincent', 'opinions': {'a': 1, 'b': -1}}),
                                 content_type='application/json')

        self.assertEqual(201, response.status_code)
        self.assertEqual('375ce742-495f-4b0c-b831-3fb0dcc61b17', server.app.bus.last_command.rangevote_id)
        self.assertEqual('Guillaume Vincent', server.app.bus.last_command.elector)
        self.assertDictEqual({'a': 1, 'b': -1}, server.app.bus.last_command.opinions)

    def test_get_results(self):
        server.app.query_dispatcher = SpyQueryDispatcher()

        response = self.app.get('/rangevotes/375ce742-495f-4b0c-b831-3fb0dcc61b17/results', content_type='application/json')

        self.assertEqual('375ce742-495f-4b0c-b831-3fb0dcc61b17', server.app.query_dispatcher.last_query.uuid)
        self.assertEqual(200, response.status_code)
