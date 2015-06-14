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

    def test_repository_find_all(self):
        self.repository.save(rangevoting.RangeVote(uuid.uuid4(), '?', ['c1', 'c2']))
        self.repository.save(rangevoting.RangeVote(uuid.uuid4(), '?', ['c1', 'c2']))

        elements = self.repository.find()

        self.assertEqual(2, len(elements))
        self.assertTrue(isinstance(elements[0], rangevoting.RangeVote))

    def test_repository_find_all_count(self):
        self.repository.save(rangevoting.RangeVote(uuid.uuid4(), '?', ['c1', 'c2']))
        self.repository.save(rangevoting.RangeVote(uuid.uuid4(), '?', ['c1', 'c2']))

        elements = self.repository.find(1)

        self.assertEqual(1, len(elements))

    def test_repository_find_all_order(self):
        self.repository.save(rangevoting.RangeVote(uuid.uuid4(), 'Q1?', ['c1', 'c2']))
        self.repository.save(rangevoting.RangeVote(uuid.uuid4(), 'Q2?', ['c1', 'c2']))

        elements = self.repository.find(1)

        self.assertEqual('Q2?', elements[0].question)
