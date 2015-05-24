import uuid
import unittest

import mongomock

from rangevoting import RangeVote, Vote
from repository import MongoRepository


class MongoRepositoryTestCase(unittest.TestCase):
    def setUp(self):
        self.database = mongomock.Connection().db
        self.repository = MongoRepository(self.database)

    def test_repository_save(self):
        rangevote = RangeVote(uuid.uuid4(), '?', ['c1', 'c2'])
        self.repository.save(rangevote)

        element = self.database.rangevote.find_one()

        self.assertEqual(rangevote.question, element['question'])
        self.assertEqual(rangevote.choices, element['choices'])

    def test_repository_get(self):
        rangevote_id = uuid.uuid4()
        rangevote = RangeVote(rangevote_id, '?', ['c1', 'c2'])
        rangevote.add_vote(Vote(elector='Guillaume', opinions={'a': 1, 'b': -2}))
        self.repository.save(rangevote)

        element = self.repository.get(rangevote_id)

        self.assertTrue(isinstance(element, RangeVote))
        self.assertEqual(rangevote.question, element.question)
        self.assertEqual(rangevote.choices, element.choices)
        self.assertEqual(rangevote.votes[0].elector, element.votes[0].elector)
        self.assertDictEqual(rangevote.votes[0].opinions, element.votes[0].opinions)

    def test_repository_update(self):
        rangevote_id = uuid.uuid4()
        rangevote = RangeVote(rangevote_id, 'Q', ['c1', 'c2'])
        self.repository.save(rangevote)

        rangevote.question = 'Q?'
        self.repository.update(rangevote.uuid, rangevote)

        element = self.repository.get(rangevote_id)
        self.assertEqual(rangevote.question, element.question)
