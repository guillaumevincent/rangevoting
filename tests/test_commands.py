import unittest

from commands import CreateRangeVoteCommand, CreateRangeVoteCommandValidator


class SpyValidator():
    def __init__(self):
        self.validate_called = False

    def validate(self, command):
        self.validate_called = True


class CommandsTestCase(unittest.TestCase):
    def test_create_rangevote_command(self):
        uid = 1
        question = 'Question ?'
        choices = ['a', 'b']

        create_rangevote_command = CreateRangeVoteCommand(uid, question, choices)

        self.assertEqual(uid, create_rangevote_command.uuid)
        self.assertEqual(question, create_rangevote_command.question)
        self.assertEqual(choices, create_rangevote_command.choices)

    def test_rangevote_validator(self):
        command_validator = CreateRangeVoteCommandValidator({'question': 'Question', 'choices': ['c1', 'c2']})
        self.assertTrue(command_validator.is_valid())

        command_validator = CreateRangeVoteCommandValidator({})
        self.assertFalse(command_validator.is_valid())

        command_validator = CreateRangeVoteCommandValidator({'question': 'Question', 'choices': ['c1']})
        self.assertFalse(command_validator.is_valid())