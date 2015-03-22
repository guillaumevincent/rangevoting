import unittest

from handlers import CreateRangeVotingHandler
from commands import CreateRangeVotingCommand
from repository import MockRepository


class HandlersTestCase(unittest.TestCase):
    def test_create_rangevoting_handler_call_save_method(self):
        mock_repository = MockRepository()
        rangevoting_handler = CreateRangeVotingHandler(mock_repository)
        rangevoting_handler.handle(CreateRangeVotingCommand('Q?', ['a', 'b']))
        self.assertTrue(mock_repository.saved_called)