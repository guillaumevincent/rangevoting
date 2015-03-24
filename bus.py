import logging

logger = logging.getLogger(__name__)


class Status():
    def __init__(self, status_code):
        self.code = status_code


class Bus():
    def __init__(self):
        self.handlers = {}

    def register(self, command, handler):
        self.handlers[command] = handler

    def send(self, command):
        command_type = type(command)
        if command_type not in self.handlers:
            raise (Exception('No handler for command ' + str(command_type) + ' found'))
        try:
            self.handlers[command_type].handle(command)
        except Exception as e:
            logger.exception(e)
            return Status(400)