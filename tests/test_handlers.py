import unittest
from unittest.mock import Mock

from handlers import RangeVotingHandler

from repository import RangeVotingRepository


class RangeVotingHandlerTestCase(unittest.TestCase):
    def test_creation(self):
        member_mock_repository = RangeVotingRepository()
        rangevoting_handler = RangeVotingHandler(member_mock_repository)
        self.assertEqual(member_mock_repository, rangevoting_handler.repository)

    def test_handle_calls_save_method_from_repository(self):
        member_mock_repository = RangeVotingRepository()
        member_mock_repository.save = Mock()

        rangevoting_handler = RangeVotingHandler(member_mock_repository)
        rangevoting_handler.handle({})

        self.assertTrue(member_mock_repository.save.called)


if __name__ == '__main__':
    unittest.main()
