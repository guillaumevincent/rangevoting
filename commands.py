class CreateRangeVoteCommand():
    def __init__(self, uuid, question, choices):
        self.uuid = uuid
        self.question = question
        self.choices = choices


class CreateRangeVoteCommandValidator():
    def __init__(self, data):
        self.data = data

    def is_valid(self):
        if 'question' not in self.data or 'choices' not in self.data:
            return False
        if len(self.data['choices']) < 2:
            return False
        return True