import unittest

from queries import GetRangeVoteQuery
from commands import CreateRangeVoteCommand
from handlers import CreateRangeVoteHandler, GetRangeVoteHandler
from repository import MockRepository


class HandlersTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_repository = MockRepository()

    def test_create_rangevote_handler_call_save_method(self):
        create_rangevote_handler = CreateRangeVoteHandler(self.mock_repository)

        create_rangevote_handler.handle(CreateRangeVoteCommand(1, 'Q?', ['a', 'b']))

        self.assertTrue(self.mock_repository.saved_called)

    def test_get_rangevote_handler_call_get_method(self):
        get_rangevote_handler = GetRangeVoteHandler(self.mock_repository)

        get_rangevote_handler.execute(GetRangeVoteQuery(1))

        self.assertTrue(self.mock_repository.get_called)