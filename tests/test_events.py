import unittest

from events import RangeVoteCreated


class EventsTestCase(unittest.TestCase):
    def test_rangevote_created_event(self):
        question = 'Question ?'
        choices = ['a', 'b']

        rangevote_created_event = RangeVoteCreated(question, choices)

        self.assertEqual(question, rangevote_created_event.question)
        self.assertEqual(choices, rangevote_created_event.choices)