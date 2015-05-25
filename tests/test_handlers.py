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

    def test_create_vote_handler_save_vote_created(self):
        self.mock_repository.db[1] = rangevoting.RangeVote(1, 'Q?', ['a', 'b'])
        create_vote_handler = handlers.CreateVoteHandler(self.mock_repository)

        create_vote_handler.handle(commands.CreateVoteCommand(1, 'GV', {'a': 1, 'b': -2}))

        self.assertEqual(1, self.mock_repository.db[1].uuid)
        self.assertEqual('GV', self.mock_repository.db[1].votes[0].elector)
        self.assertDictEqual({'a': 1, 'b': -2}, self.mock_repository.db[1].votes[0].opinions)


class QueryHandlersTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_repository = repository.MockRepository()

    def test_get_rangevote_handler(self):
        self.mock_repository.db[1] = rangevoting.RangeVote(1, 'Q?', ['a', 'b'])
        get_rangevote_handler = handlers.GetRangeVoteHandler(self.mock_repository)

        rangevote = get_rangevote_handler.handle(queries.GetRangeVoteQuery(1))

        expected_rangevote = self.mock_repository.db[1].serialize()

        self.assertEqual(expected_rangevote['id'], rangevote['id'])
        self.assertEqual(expected_rangevote['question'], rangevote['question'])
        self.assertListEqual(expected_rangevote['choices'], rangevote['choices'])

    def test_get_rangevote_results_handler(self):
        self.mock_repository.db[1] = rangevoting.RangeVote(1, 'Q?', ['a', 'b'])
        self.mock_repository.db[1].votes = [{'a': 1, 'b': -1}, {'a': -1}, {'a': -2, 'b': 1}]
        get_rangevote_results_handler = handlers.GetRangeVoteResultsHandler(self.mock_repository)

        results = get_rangevote_results_handler.handle(queries.GetRangeVoteResultsQuery(1))
        expected_results = {
            'question': 'Q?',
            'answers': ['b'],
            'counting': {'a': -2, 'b': 0},
            'number_of_votes': 3
        }
        self.assertDictEqual(results, expected_results)
