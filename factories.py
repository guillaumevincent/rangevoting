from rangevoting import RangeVote, Vote


class RangeVoteFactory:
    @staticmethod
    def create_rangevote(rangevote_dict):
        rangevote = RangeVote(uuid=rangevote_dict['id'], question=rangevote_dict['question'], choices=rangevote_dict['choices'])
        votes = []
        for vote in rangevote_dict['votes']:
            votes.append(Vote(elector=vote['elector'], opinions=vote['opinions']))
        rangevote.votes = votes
        return rangevote
