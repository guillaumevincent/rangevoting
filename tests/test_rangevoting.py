import unittest

from rangevoting import Vote, RangeVoting


class VoteTestCase(unittest.TestCase):
    def test_has_elector(self):
        elector = 'Guillaume Vincent'
        vote = Vote(elector, {})
        self.assertEqual(elector, vote.elector)

    def test_has_opinions(self):
        opinions = {'first opinion': 2, 'second opinion': 0}
        vote = Vote('', opinions)
        self.assertEqual(opinions, vote.opinions)


class RangeVotingTestCase(unittest.TestCase):
    def test_has_id(self):
        rangevoting = RangeVoting('', [])
        self.assertIsNone(rangevoting.id)

    def test_has_a_question(self):
        question = "What am I going to cook tonight?"
        rangevoting = RangeVoting(question, [])
        self.assertEqual(question, rangevoting.question)

    def test_has_choices(self):
        choices = ['first choice', 'second choice']
        rangevoting = RangeVoting('', choices)
        self.assertEqual(choices, rangevoting.choices)

    def test_has_votes(self):
        rangevoting = RangeVoting('', [])
        self.assertEqual([], rangevoting.votes)

    def test_can_add_vote(self):
        vote = Vote('Guillaume Vincent', {'a': 0, 'b': 0})
        rangevoting = RangeVoting('', [])
        rangevoting.add_vote(vote)
        self.assertEqual([vote], rangevoting.votes)

    def test_get_results_equal_to_choices_if_no_votes(self):
        choices = ['a', 'b']
        rangevoting = RangeVoting('', choices)
        results = rangevoting.get_results()
        self.assertEqual(choices, results)

    def test_get_results_with_one_winner(self):
        rangevoting = RangeVoting('', [])
        counting = {'a': 2, 'b': 1}
        results = rangevoting.get_results(counting)
        self.assertEqual(['a'], results)

    def test_get_results_with_equality(self):
        rangevoting = RangeVoting('', [])
        equality = {'a': 1, 'b': 1}
        results = rangevoting.get_results(equality)
        self.assertCountEqual(['a', 'b'], results)

    def test_counting(self):
        rangevoting = RangeVoting('', [])
        counting = rangevoting.counting([{'a': 0, 'b': 1, 'c': -1}, {'a': 1, 'b': 0, 'c': 2}])
        self.assertEqual({'a': 1, 'b': 1, 'c': 1}, counting)