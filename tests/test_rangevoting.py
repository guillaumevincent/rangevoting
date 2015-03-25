import unittest

from rangevoting import Vote, RangeVote


class VoteTestCase(unittest.TestCase):
    def test_has_elector(self):
        elector = 'Guillaume Vincent'

        vote = Vote(elector, {})

        self.assertEqual(elector, vote.elector)

    def test_has_opinions(self):
        opinions = {'first opinion': 2, 'second opinion': 0}

        vote = Vote('', opinions)

        self.assertEqual(opinions, vote.opinions)


class RangeVoteTestCase(unittest.TestCase):
    def test_has_id(self):
        rangevote = RangeVote(1, '', [])

        self.assertEqual(1, rangevote.uid)

    def test_has_a_question(self):
        question = "What am I going to cook tonight?"
        rangevote = RangeVote(1, question, [])

        self.assertEqual(question, rangevote.question)

    def test_has_choices(self):
        choices = ['first choice', 'second choice']
        rangevote = RangeVote(1, '', choices)

        self.assertEqual(choices, rangevote.choices)

    def test_has_votes(self):
        rangevote = RangeVote(1, '', [])

        self.assertEqual([], rangevote.votes)

    def test_can_add_vote(self):
        vote = Vote('Guillaume Vincent', {'a': 0, 'b': 0})
        rangevote = RangeVote(1, '', [])

        rangevote.add_vote(vote)

        self.assertEqual([vote], rangevote.votes)

    def test_get_results_equal_to_choices_if_no_votes(self):
        choices = ['a', 'b']
        rangevote = RangeVote(1, '', choices)

        results = rangevote.get_results()

        self.assertEqual(choices, results)

    def test_get_results_with_one_winner(self):
        rangevote = RangeVote(1, '', [])
        counting = {'a': 2, 'b': 1}

        results = rangevote.get_results(counting)

        self.assertEqual(['a'], results)

    def test_get_results_with_two_winners(self):
        rangevote = RangeVote(1, '', [])
        counting = {'a': 2, 'b': 1, 'c': 2}

        results = rangevote.get_results(counting)

        self.assertEqual(sorted(['a', 'c']), sorted(results))

    def test_get_results_with_equality(self):
        rangevote = RangeVote(1, '', [])
        equality = {'a': 1, 'b': 1}

        results = rangevote.get_results(equality)

        self.assertCountEqual(['a', 'b'], results)

    def test_counting(self):
        rangevote = RangeVote(1, '', [])

        counting = rangevote.counting([{'a': 0, 'b': 1, 'c': -1}, {'a': 1, 'b': 0, 'c': 2}])

        self.assertEqual({'a': 1, 'b': 1, 'c': 1}, counting)