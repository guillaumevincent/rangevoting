import logging

logger = logging.getLogger(__name__)


class RangeVoteCommandValidator():
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


class RangeVoteCommand():
    def __init__(self, uuid, question, choices):
        self.uuid = uuid
        self.question = question
        self.choices = choices


class CreateRangeVoteCommand(RangeVoteCommand):
    pass


class UpdateRangeVoteCommand(RangeVoteCommand):
    pass

