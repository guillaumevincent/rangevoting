import unittest

from bus import Bus


class FakeHandler():
    def __init__(self):
        self.handle_called = False
        self.command = None

    def handle(self, command):
        self.handle_called = True
        self.command = command


class BusTestCase(unittest.TestCase):
    def test_bus_can_register_handler(self):
        bus = Bus()
        command = object
        handler = object()
        bus.register(command, handler)
        self.assertTrue(command in bus.handlers)
        self.assertEqual(handler, bus.handlers[command])

    def test_send_execute_handle_method_from_handler(self):
        bus = Bus()
        handler = FakeHandler()
        bus.register(object, handler)
        command = object()
        bus.send(command)
        self.assertTrue(handler.handle_called)
        self.assertEqual(command, handler.command)

    def test_raise_error_if_no_handlers_availables(self):
        bus = Bus()
        with self.assertRaises(Exception):
            bus.send(object())