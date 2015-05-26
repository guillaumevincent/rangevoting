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

    def _get_counting(self):
        c = collections.Counter()
        for vote in self.votes:
            c.update(vote.opinions)
        return c

    def get_answers(self):
        counting = self._get_counting()
        if not counting:
            return []
        highest_note = max(counting.values())
        answers = []
        for key, value in counting.items():
            if value == highest_note:
                answers.append(key)
        return answers

    def get_ranking(self):
        counting = self._get_counting()
        if not counting:
            return []
        ranking = []
        for choice in sorted(counting, key=counting.get, reverse=True):
            ranking.append({'choice': choice, 'score': counting[choice]})
        return ranking

    def _get_serialized_votes(self):
        returned_votes = []
        for vote in self.votes:
            returned_votes.append(vote.serialize())
        return returned_votes

    def serialize(self):
        new_choices = list(self.choices)
        random.shuffle(new_choices)
        return {'id': str(self.uuid), 'question': self.question, 'choices': self.choices, 'votes': self._get_serialized_votes(),
                'randomized_choices': new_choices}


class Vote:
    def __init__(self, elector, opinions):
        self.elector = elector
        self.opinions = opinions

    def serialize(self):
        return {'elector': self.elector, 'opinions': self.opinions}
