import uuid
import unittest

import mongomock
from factories import RangeVoteFactory

import repository
import rangevoting


class MongoRepositoryTestCase(unittest.TestCase):
    def setUp(self):
        self.database = mongomock.Connection().db
        self.repository = repository.MongoRepository(self.database)

    def test_repository_save(self):
        rangevote = rangevoting.RangeVote(uuid.uuid4(), '?', ['c1', 'c2'])
        self.repository.save(rangevote)

        element = self.database.rangevote.find_one()

        self.assertEqual(rangevote.question, element['question'])
        self.assertEqual(rangevote.choices, element['choices'])

    def test_repository_get(self):
        rangevote_id = uuid.uuid4()
        rangevote = RangeVoteFactory.create_rangevote({
            "id": rangevote_id,
            "choices": ["a", "b"],
            "votes": [{"opinions": {"a": 1, "b": 2}, "elector": "G"}, {"opinions": {"a": 0, "b": 0}, "elector": "C"}],
            'question': 'Q'
        })
        self.repository.save(rangevote)

        element = self.repository.get(rangevote_id)

        self.assertTrue(isinstance(element, rangevoting.RangeVote))
        self.assertEqual(rangevote.question, element.question)
        self.assertEqual(rangevote.choices, element.choices)
        self.assertEqual(rangevote.votes[0].elector, element.votes[0].elector)
        self.assertDictEqual(rangevote.votes[0].opinions, element.votes[0].opinions)

    def test_repository_update(self):
        rangevote_id = uuid.uuid4()
        rangevote = RangeVoteFactory.create_rangevote({
            "id": rangevote_id,
            "choices": ["a", "b"],
            "votes": [{"opinions": {"a": 1, "b": 2}, "elector": "G"}, {"opinions": {"a": 0, "b": 0}, "elector": "C"}],
            'question': 'Q'
        })
        self.repository.save(rangevote)

        updated_rangevote = RangeVoteFactory.create_rangevote({
            "id": rangevote_id,
            "choices": ["a", "b"],
            "votes": [{"opinions": {"a": 1, "b": 2}, "elector": "G"}],
            'question': 'Q?'
        })
        self.repository.update(rangevote_id, updated_rangevote)

        element = self.repository.get(rangevote_id)
        self.assertEqual(updated_rangevote.question, element.question)
        self.assertEqual(len(updated_rangevote.votes), len(element.votes))
