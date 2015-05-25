import random
import collections


class RangeVote:
    def __init__(self, uuid, question, choices):
        self.uuid = uuid
        self.question = question
        self.choices = choices
        self.votes = []

    def add_vote(self, vote):
        self.votes.append(vote)

    def get_answers(self, counting=None):
        if counting:
            highest_note = max(counting.values())
            answers = []
            for key, value in counting.items():
                if value >= highest_note:
                    answers.append(key)
            return answers
        return self.choices

    @staticmethod
    def counting(votes):
        c = collections.Counter()
        for vote in votes:
            c.update(vote)
        return c

    def serialize(self):
        new_choices = list(self.choices)
        random.shuffle(new_choices)
        return {'id': str(self.uuid), 'question': self.question, 'choices': self.choices, 'votes': self.get_serialized_votes(),
                'randomized_choices': new_choices}

    def get_serialized_votes(self):
        returned_votes = []
        for vote in self.votes:
            returned_votes.append(vote.serialize())
        return returned_votes


class Vote:
    def __init__(self, elector, opinions):
        self.elector = elector
        self.opinions = opinions

    def serialize(self):
        return {'elector': self.elector, 'opinions': self.opinions}
