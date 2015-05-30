import logging

logger = logging.getLogger(__name__)


class RangeVoteCommandValidator:
    def __init__(self, data):
        self.data = data

    def is_valid(self):
        if 'question' not in self.data or 'choices' not in self.data:
            logger.debug('RangeVoteCommandValidator : question or choices not in rangevote')
            return False
        if len(self.data['choices']) < 2:
            logger.debug('RangeVoteCommandValidator : should have at least two choices in rangevote')
            return False
        return True


class RangeVoteCommand:
    def __init__(self, uuid, question, choices):
        self.uuid = uuid
        self.question = question
        self.choices = choices


class CreateRangeVoteCommand(RangeVoteCommand):
    pass


class UpdateRangeVoteCommand(RangeVoteCommand):
    def __init__(self, uuid, question, choices, votes):
        self.votes = votes
        super().__init__(uuid, question, choices)


class VoteCommandValidator:
    def __init__(self, data):
        self.data = data

    def is_valid(self):
        if 'elector' not in self.data or 'opinions' not in self.data:
            logger.debug('RangeVoteCommandValidator : elector or opinions not in vote ({0})'.format(self.data))
            return False
        return True


class CreateVoteCommand:
    def __init__(self, rangevote_id, elector, opinions):
        self.rangevote_id = rangevote_id
        self.elector = elector
        self.opinions = opinions
