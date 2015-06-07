import logging

logger = logging.getLogger(__name__)


class Result:
    def __init__(self):
        self.ok = True

    def ok(self):
        return self.ok


class BadResult(Result):
    def __init__(self):
        super().__init__()
        self.ok = False


class Bus:
    def __init__(self):
        self.handlers = {}

    def register(self, action, handler):
        self.handlers[action] = handler

    def handle(self, action, action_type):
        try:
            self.handlers[action_type].handle(action)
            return Result()
        except Exception as e:
            logger.exception(e)
            return BadResult()

    def execute(self, action):
        action_type = type(action)
        if action_type not in self.handlers:
            raise Exception('No handler for action ' + str(action_type) + ' found')

        return self.handle(action, action_type)


class QueryDispatcher(Bus):
    def handle(self, query, query_type):
        try:
            return self.handlers[query_type].handle(query)
        except Exception as e:
            logger.exception(e)
            return None
