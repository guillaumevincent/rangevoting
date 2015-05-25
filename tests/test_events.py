import unittest

import events


class EventsTestCase(unittest.TestCase):
    def test_rangevote_created_event(self):
        question = 'Question ?'
        choices = ['a', 'b']

        rangevote_created_event = events.RangeVoteCreated(question, choices)

        self.assertEqual(question, rangevote_created_event.question)
        self.assertEqual(choices, rangevote_created_event.choices)
