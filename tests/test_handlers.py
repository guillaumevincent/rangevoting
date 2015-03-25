import unittest

from handlers import CreateRangeVoteHandler
from commands import CreateRangeVoteCommand
from repository import MockRepository


class HandlersTestCase(unittest.TestCase):
    def test_create_rangevote_handler_call_save_method(self):
        mock_repository = MockRepository()
        rangevote_handler = CreateRangeVoteHandler(mock_repository)

        rangevote_handler.handle(CreateRangeVoteCommand(1, 'Q?', ['a', 'b']))

        self.assertTrue(mock_repository.saved_called)