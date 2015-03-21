import unittest

from events import RangeVotingCreated


class EventsTestCase(unittest.TestCase):
    def test_rangevoting_created_event(self):
        question = 'Question ?'
        choices = ['a', 'b']
        rangevoting_created_event = RangeVotingCreated(question, choices)
        self.assertEqual(question, rangevoting_created_event.question)
        self.assertEqual(choices, rangevoting_created_event.choices)