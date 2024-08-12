import unittest.mock

from domain.driven_port.actionizer import Actionizer
from domain.driven_port.answerer import Answerer
from domain.driving_port.instructor import DomainInstructor


def test_instructor_should_call_actionizer():
    actionizer = unittest.mock.create_autospec(
        Actionizer, instance=True
    )
    answerer = unittest.mock.create_autospec(
        Answerer, instance=True
    )

    instructor = DomainInstructor(actionizer, answerer)
    instructor.instruct("Dummy")

    actionizer.read_book.assert_called_once_with("Dummy")
