import unittest
import uuid

import rangevoting


class VoteTestCase(unittest.TestCase):
    def test_has_elector(self):
        elector = 'Guillaume Vincent'

        vote = rangevoting.Vote(elector, {})

        self.assertEqual(elector, vote.elector)

    def test_has_opinions(self):
        opinions = {'first opinion': 2, 'second opinion': 0}

        vote = rangevoting.Vote('', opinions)

        self.assertEqual(opinions, vote.opinions)

    def test_serialize_method(self):
        vote = rangevoting.Vote('GV', {'a': 1, 'b': -2})
        expected_vote = {'elector': 'GV', 'opinions': {'a': 1, 'b': -2}}
        self.assertDictEqual(expected_vote, vote.serialize())


class RangeVoteTestCase(unittest.TestCase):
    def test_has_id(self):
        rangevote = rangevoting.RangeVote(1, '', [])

        self.assertEqual(1, rangevote.uuid)

    def test_has_a_question(self):
        question = "What am I going to cook tonight?"
        rangevote = rangevoting.RangeVote(1, question, [])

        self.assertEqual(question, rangevote.question)

    def test_has_choices(self):
        choices = ['first choice', 'second choice']
        rangevote = rangevoting.RangeVote(1, '', choices)

        self.assertEqual(choices, rangevote.choices)

    def test_has_votes(self):
        rangevote = rangevoting.RangeVote(1, '', [])

        self.assertEqual([], rangevote.votes)

    def test_can_add_vote(self):
        vote = rangevoting.Vote('Guillaume Vincent', {'a': 0, 'b': 0})
        rangevote = rangevoting.RangeVote(1, '', [])

        rangevote.add_vote(vote)

        self.assertEqual([vote], rangevote.votes)

    def test_get_answers_equal_to_choices_if_no_votes(self):
        choices = ['a', 'b']
        rangevote = rangevoting.RangeVote(1, '', choices)

        answers = rangevote.get_answers()

        self.assertEqual(choices, answers)

    def test_get_answers_with_one_winner(self):
        rangevote = rangevoting.RangeVote(1, '', [])
        rangevote.add_vote({'a': 2, 'b': 1})

        answers = rangevote.get_answers()

        self.assertEqual(['a'], answers)

    def test_get_answers_with_two_winners(self):
        rangevote = rangevoting.RangeVote(1, '', [])
        rangevote.add_vote({'a': 2, 'b': 1, 'c': 2})

        answers = rangevote.get_answers()

        self.assertEqual(sorted(['a', 'c']), sorted(answers))

    def test_get_answers_with_equality(self):
        rangevote = rangevoting.RangeVote(1, '', [])
        rangevote.add_vote({'a': 1, 'b': 1})

        answers = rangevote.get_answers()

        self.assertCountEqual(['a', 'b'], answers)

    def test_get_answer_with_two_votes(self):
        rangevote = rangevoting.RangeVote(1, '', [])
        rangevote.add_vote({'a a': 0, 'b': 1, 'c': -1})
        rangevote.add_vote({'a a': 1, 'b': 0, 'c': 2})

        answers = rangevote.get_answers()

        self.assertListEqual(sorted(['a a', 'b', 'c']), sorted(answers))

    def test_serialize_method(self):
        rangevote_id = uuid.uuid4()
        rangevote = rangevoting.RangeVote(rangevote_id, 'Q?', ['a', 'b'])
        rangevote.add_vote(rangevoting.Vote(elector='Guillaume', opinions={'a': 1, 'b': -2}))
        rangevote.add_vote(rangevoting.Vote(elector='Vincent', opinions={'a': 0, 'b': -2}))
        serialize_rangevote = rangevote.serialize()

        self.assertEqual(str(rangevote_id), serialize_rangevote['id'])
        self.assertEqual(rangevote.question, serialize_rangevote['question'])
        self.assertEqual(rangevote.choices, serialize_rangevote['choices'])
        self.assertEqual(set(rangevote.choices), set(serialize_rangevote['randomized_choices']))
        self.assertEqual([{'elector': 'Guillaume', 'opinions': {'a': 1, 'b': -2}}, {'elector': 'Vincent', 'opinions': {'a': 0, 'b': -2}}],
                         serialize_rangevote['votes'])

    def test_serialize_method_add_randomized_choices(self):
        choices = [str(c) for c in range(0, 100)]
        rangevote = rangevoting.RangeVote(uuid.uuid4(), 'Q?', choices)

        first_choices = rangevote.serialize()['randomized_choices']
        second_choices = rangevote.serialize()['randomized_choices']

        self.assertNotEqual(first_choices, second_choices)
        self.assertEqual(set(first_choices), set(second_choices))
