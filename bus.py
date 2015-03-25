import logging

logger = logging.getLogger(__name__)


class Result():
    def __init__(self):
        self.ok = True

    def ok(self):
        return self.ok


class BadResult(Result):
    def __init__(self):
        super().__init__()
        self.ok = False


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
            return Result()
        except Exception as e:
            logger.exception(e)
            return BadResult()