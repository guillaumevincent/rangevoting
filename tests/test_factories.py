import unittest

from factories import RangeVoteFactory


class FactoryTestCase(unittest.TestCase):
    def test_rangevote_factory(self):
        rangevote_dict = {
            "id": "f1c9f71e-a6f0-46bf-8cf3-d9b8f01c0005",
            "choices": [
                "Chinoise",
                "Italienne",
                "Française"
            ],
            "votes": [
                {
                    "opinions": {
                        "Chinoise": 1,
                        "Française": 2,
                        "Italienne": 1
                    },
                    "elector": "Guillaume"
                },
                {
                    "opinions": {
                        "Chinoise": 0,
                        "Française": 0,
                        "Italienne": 0
                    },
                    "elector": "Carine"
                }
            ],
            "question": "Quel type de cusine préférez vous ?"
        }

        rangevote = RangeVoteFactory.create_rangevote(rangevote_dict)

        self.assertEqual('f1c9f71e-a6f0-46bf-8cf3-d9b8f01c0005', rangevote.uuid)
        self.assertEqual('Quel type de cusine préférez vous ?', rangevote.question)
        self.assertEqual(["Chinoise", "Italienne", "Française"], rangevote.choices)
        self.assertEqual('Guillaume', rangevote.votes[0].elector)
        self.assertEqual("Carine", rangevote.votes[1].elector)
        self.assertEqual({"Chinoise": 1, "Française": 2, "Italienne": 1}, rangevote.votes[0].opinions)
        self.assertEqual({"Chinoise": 0, "Française": 0, "Italienne": 0}, rangevote.votes[1].opinions)
