import unittest
import uuid

import rangevoting


class TestVote(rangevoting.Vote):
    def __init__(self, elector='Guillaume Vincent', opinions=None):
        if opinions is None:
            opinions = {'a': 1, 'b': -2}
        super().__init__(elector, opinions)


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


class TestRangeVote(rangevoting.RangeVote):
    def __init__(self, uid=uuid.uuid4(), question='Q?', choices=None, votes=None):
        if choices is None:
            choices = ['a', 'b']
        super().__init__(uid, question, choices)
        if votes is not None:
            self.votes = votes


class RangeVoteTestCase(unittest.TestCase):
    def test_rangevote_has_unique_identifier_created_during_its_creation(self):
        rangevote = rangevoting.RangeVote(1, 'Q?', ['a', 'b'])

        self.assertIsNotNone(rangevote.uuid)

    def test_rangevote_has_question_and_choices_attributes(self):
        question = 'Q?'
        choices = ['a', 'b']
        rangevote = rangevoting.RangeVote(1, question, choices)

        self.assertEqual(question, rangevote.question)
        self.assertEqual(choices, rangevote.choices)

    def test_has_empty_votes_attributes(self):
        rangevote = rangevoting.RangeVote(1, 'Q?', ['a', 'b'])

        self.assertEqual([], rangevote.votes)

    def test_can_add_vote(self):
        rangevote = TestRangeVote()

        rangevote.add_vote(TestVote())

        self.assertEqual(1, len(rangevote.votes))

    def test_get_no_answers_if_no_votes(self):
        rangevote = TestRangeVote()

        answers = rangevote.get_answers()

        self.assertCountEqual([], answers)

    def test_better_answer_win_with_one_vote(self):
        rangevote = TestRangeVote(votes=[TestVote(opinions={'a': 1, 'b': -2})])

        answers = rangevote.get_answers()

        self.assertCountEqual(['a'], answers)

    def test_better_answer_win_with_two_votes(self):
        rangevote = TestRangeVote(votes=[TestVote(opinions={'a': 2, 'b': -2}), TestVote(opinions={'a': -2, 'b': 1})])

        answers = rangevote.get_answers()

        self.assertCountEqual(['a'], answers)

    def test_equality_with_one_vote(self):
        rangevote = TestRangeVote(votes=[TestVote(opinions={'a': 1, 'b': 1})])

        answers = rangevote.get_answers()

        self.assertCountEqual(['a', 'b'], answers)

    def test_equality_with_two_votes(self):
        rangevote = TestRangeVote(votes=[TestVote(opinions={'a': 1, 'b': -2}), TestVote(opinions={'a': -2, 'b': 1})])

        answers = rangevote.get_answers()

        self.assertCountEqual(['a', 'b'], answers)

    def test_get_ranking(self):
        rangevote = TestRangeVote(votes=[TestVote(opinions={'a': 1, 'b': 2}), TestVote(opinions={'a': -2, 'b': 1})])

        answers = rangevote.get_ranking()

        self.assertListEqual([{'choice': 'b', 'score': 3}, {'choice': 'a', 'score': -1}], answers)

    def test_serialize_method(self):
        rangevote = TestRangeVote(
            votes=[rangevoting.Vote(elector='G', opinions={'a': 1, 'b': -2}), rangevoting.Vote(elector='V', opinions={'a': 0, 'b': -2})])

        serialize_rangevote = rangevote.serialize()

        self.assertEqual(str(rangevote.uuid), serialize_rangevote['id'])
        self.assertEqual(rangevote.question, serialize_rangevote['question'])
        self.assertEqual(rangevote.choices, serialize_rangevote['choices'])
        self.assertEqual(set(rangevote.choices), set(serialize_rangevote['randomized_choices']))
        self.assertEqual([{'elector': 'G', 'opinions': {'a': 1, 'b': -2}}, {'elector': 'V', 'opinions': {'a': 0, 'b': -2}}],
                         serialize_rangevote['votes'])

    def test_serialize_method_add_randomized_choices(self):
        choices = [str(c) for c in range(0, 100)]
        rangevote = TestRangeVote(1, 'Q?', choices)

        first_choices = rangevote.serialize()['randomized_choices']
        second_choices = rangevote.serialize()['randomized_choices']

        self.assertNotEqual(first_choices, second_choices)
        self.assertEqual(set(first_choices), set(second_choices))
