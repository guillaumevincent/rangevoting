import unittest

from rangevoting import RangeVote
from queries import GetRangeVoteQuery
from repository import MockRepository
from commands import CreateRangeVoteCommand, UpdateRangeVoteCommand
from handlers import CreateRangeVoteHandler, GetRangeVoteHandler, UpdateRangeVoteHandler


class HandlersTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_repository = MockRepository()

    def test_create_rangevote_handler_save_rangevote_created(self):
        create_rangevote_handler = CreateRangeVoteHandler(self.mock_repository)

        create_rangevote_handler.handle(CreateRangeVoteCommand(1, 'Q?', ['a', 'b']))

        self.assertEqual(1, self.mock_repository.saved_element.uuid)
        self.assertEqual('Q?', self.mock_repository.saved_element.question)
        self.assertEqual(['a', 'b'], self.mock_repository.saved_element.choices)

    def test_update_rangevote_handler_call_update_method(self):
        update_rangevote_handler = UpdateRangeVoteHandler(self.mock_repository)

        update_rangevote_handler.handle(UpdateRangeVoteCommand(1, 'Q?', ['a', 'b']))

        self.assertEqual(1, self.mock_repository.saved_element.uuid)
        self.assertEqual('Q?', self.mock_repository.saved_element.question)
        self.assertEqual(['a', 'b'], self.mock_repository.saved_element.choices)

    def test_get_rangevote_handler_call_get_method(self):
        get_rangevote_handler = GetRangeVoteHandler(self.mock_repository)
        self.mock_repository.saved_element = RangeVote(1, 'Q?', ['a', 'b'])

        element = get_rangevote_handler.handle(GetRangeVoteQuery(1))

        self.assertEqual(self.mock_repository.saved_element, element)