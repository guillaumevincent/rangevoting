import logging
import unittest

import bus


class FakeHandler:
    def __init__(self):
        self.handle_called = False
        self.command = None

    def handle(self, command):
        self.handle_called = True
        self.command = command


class RaiseExceptionHandler:
    def __init__(self):
        pass

    @staticmethod
    def handle(command):
        raise Exception


class BusTestCase(unittest.TestCase):
    def setUp(self):
        root = logging.getLogger()
        root.setLevel(logging.CRITICAL)

    def test_bus_can_register_handler(self):
        b = bus.Bus()
        command = object
        handler = object()

        b.register(command, handler)

        self.assertTrue(command in b.handlers)
        self.assertEqual(handler, b.handlers[command])

    def test_execute_handle_method_from_handler(self):
        b = bus.Bus()
        handler = FakeHandler()
        b.register(object, handler)
        command = object()

        b.execute(command)

        self.assertTrue(handler.handle_called)
        self.assertEqual(command, handler.command)

    def test_handler_raise_exception_in_execute_method(self):
        b = bus.Bus()
        b.register(object, RaiseExceptionHandler())
        command = object()

        result = b.execute(command)

        self.assertFalse(result.ok)

    def test_raise_error_if_no_handlers_availables(self):
        b = bus.Bus()
        with self.assertRaises(Exception):
            b.execute(object())
