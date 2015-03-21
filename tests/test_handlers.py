import unittest

from handlers import CreateRangeVotingHandler
from tests.test_commands import CreateRangeVotingCommand


class MockRepository():
    def __init__(self):
        self.saved_called = False

    def save(self, aggregate):
        self.saved_called = True


class CreateRangeVotingHandlerTestCase(unittest.TestCase):
    def test_rangevoting_handler_call_save_method(self):
        mock_repository = MockRepository()
        rangevoting_handler = CreateRangeVotingHandler(mock_repository)
        rangevoting_handler.handle(CreateRangeVotingCommand('Q?', ['a', 'b']))
        self.assertTrue(mock_repository.saved_called)


if __name__ == '__main__':
    unittest.main()
