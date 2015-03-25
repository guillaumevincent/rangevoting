import unittest

from commands import CreateRangeVotingCommand, CreateRangeVotingCommandValidator


class SpyValidator():
    def __init__(self):
        self.validate_called = False

    def validate(self, command):
        self.validate_called = True


class CommandsTestCase(unittest.TestCase):
    def test_create_rangevoting_command(self):
        uid = 1
        question = 'Question ?'
        choices = ['a', 'b']

        create_rangevoting_command = CreateRangeVotingCommand(uid, question, choices)

        self.assertEqual(uid, create_rangevoting_command.uuid)
        self.assertEqual(question, create_rangevoting_command.question)
        self.assertEqual(choices, create_rangevoting_command.choices)

    def test_rangevoting_validator(self):
        command_validator = CreateRangeVotingCommandValidator({'question': 'Question', 'choices': ['c1', 'c2']})
        self.assertTrue(command_validator.is_valid())

        command_validator = CreateRangeVotingCommandValidator({})
        self.assertFalse(command_validator.is_valid())

        command_validator = CreateRangeVotingCommandValidator({'question': 'Question', 'choices': ['c1']})
        self.assertFalse(command_validator.is_valid())