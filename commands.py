class CreateRangeVotingCommand():
    def __init__(self, question, choices):
        self.question = question
        self.choices = choices


class CreateRangeVotingCommandValidator():
    def __init__(self, data):
        self.data = data

    def is_valid(self):
        if 'question' not in self.data or 'choices' not in self.data:
            return False
        if len(self.data['choices']) < 2:
            return False
        return True