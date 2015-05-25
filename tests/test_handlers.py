import unittest

import queries
import handlers
import commands
import repository
import rangevoting


class HandlersTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_repository = repository.MockRepository()

    def test_create_rangevote_handler_save_rangevote_created(self):
        create_rangevote_handler = handlers.CreateRangeVoteHandler(self.mock_repository)

        create_rangevote_handler.handle(commands.CreateRangeVoteCommand(1, 'Q?', ['a', 'b']))

        self.assertEqual(1, self.mock_repository.db[1].uuid)
        self.assertEqual('Q?', self.mock_repository.db[1].question)
        self.assertEqual(['a', 'b'], self.mock_repository.db[1].choices)

    def test_update_rangevote_handler_call_update_method(self):
        update_rangevote_handler = handlers.UpdateRangeVoteHandler(self.mock_repository)

        update_rangevote_handler.handle(commands.UpdateRangeVoteCommand(1, 'Q?', ['a', 'b']))

        self.assertEqual(1, self.mock_repository.db[1].uuid)
        self.assertEqual('Q?', self.mock_repository.db[1].question)
        self.assertEqual(['a', 'b'], self.mock_repository.db[1].choices)

    def test_get_rangevote_handler_call_get_method(self):
        get_rangevote_handler = handlers.GetRangeVoteHandler(self.mock_repository)
        self.mock_repository.db[1] = rangevoting.RangeVote(1, 'Q?', ['a', 'b'])

        element = get_rangevote_handler.handle(queries.GetRangeVoteQuery(1))

        self.assertEqual(self.mock_repository.db[1], element)

    def test_create_vote_handler_save_vote_created(self):
        self.mock_repository.db[1] = rangevoting.RangeVote(1, 'Q?', ['a', 'b'])
        create_vote_handler = handlers.CreateVoteHandler(self.mock_repository)

        create_vote_handler.handle(commands.CreateVoteCommand(1, 'GV', {'a': 1, 'b': -2}))

        self.assertEqual(1, self.mock_repository.db[1].uuid)
        self.assertEqual('GV', self.mock_repository.db[1].votes[0].elector)
        self.assertDictEqual({'a': 1, 'b': -2}, self.mock_repository.db[1].votes[0].opinions)
