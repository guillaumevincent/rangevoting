import collections


class RangeVote():
    def __init__(self, uuid, question, choices):
        self.uuid = uuid
        self.question = question
        self.choices = choices
        self.votes = []

    def add_vote(self, vote):
        self.votes.append(vote)

    def get_results(self, counting=None):
        if counting:
            highest_note = max(counting.values())
            results = []
            for key, value in counting.items():
                if value >= highest_note:
                    results.append(key)
            return results
        return self.choices

    @staticmethod
    def counting(votes):
        c = collections.Counter()
        for vote in votes:
            c.update(vote)
        return c

    def serialize(self):
        return {'id': str(self.uuid), 'question': self.question, 'choices': self.choices, 'votes': self.votes}


class Vote():
    def __init__(self, elector, opinions):
        self.elector = elector
        self.opinions = opinions