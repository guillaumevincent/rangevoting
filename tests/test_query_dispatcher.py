import logging
import unittest

from bus import QueryDispatcher


logger = logging.getLogger(__name__)


class FakeHandler():
    def __init__(self):
        self.handle_called = False
        self.query = None

    def handle(self, query):
        self.handle_called = True
        self.query = query


class RaiseExceptionHandler():
    def __init__(self):
        pass

    def handle(self, query):
        raise Exception


class QueryDispatcherTestCase(unittest.TestCase):
    def setUp(self):
        root = logging.getLogger()
        root.setLevel(logging.CRITICAL)

    def test_bus_can_register_query(self):
        query_dispatcher = QueryDispatcher()
        query = object
        handler = object()

        query_dispatcher.register(query, handler)

        self.assertTrue(query in query_dispatcher.handlers)
        self.assertEqual(handler, query_dispatcher.handlers[query])

    def test_send_execute_handle_method_from_handler(self):
        query_dispatcher = QueryDispatcher()
        handler = FakeHandler()
        query_dispatcher.register(object, handler)
        query = object()

        query_dispatcher.execute(query)

        self.assertTrue(handler.handle_called)
        self.assertEqual(query, handler.query)

    def test_handler_raise_exception_in_send_method(self):
        query_dispatcher = QueryDispatcher()
        query_dispatcher.register(object, RaiseExceptionHandler())
        query = object()

        result = query_dispatcher.execute(query)

        self.assertIsNone(result)

    def test_raise_error_if_no_handlers_availables(self):
        query_dispatcher = QueryDispatcher()
        with self.assertRaises(Exception):
            query_dispatcher.execute(object())