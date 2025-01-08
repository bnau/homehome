import unittest.mock

from domain.driven_port.actionizer import Actionizer
from domain.driven_port.answerer import Answerer
from domain.driving_port.instructor import DomainInstructor
from driven.inmemory.metadata_retriever import InMemoryMetadataRetriever


def test_instructor_should_call_actionizer():
    actionizer = unittest.mock.create_autospec(
        Actionizer, instance=True
    )
    answerer = unittest.mock.create_autospec(
        Answerer, instance=True
    )
    metadataRetriever = InMemoryMetadataRetriever()

    instructor = DomainInstructor(actionizer, answerer, metadataRetriever)
    instructor.instruct("Lis un livre de Chateaubriand")

    actionizer.read_book.assert_called_once_with("Chateaubriand")


def test_instructor_with_embedding():
    actionizer = unittest.mock.create_autospec(
        Actionizer, instance=True
    )
    answerer = unittest.mock.create_autospec(
        Answerer, instance=True
    )
    metadataRetriever = InMemoryMetadataRetriever()

    instructor = DomainInstructor(actionizer, answerer, metadataRetriever)
    instructor.instruct("Joue the mountain par haken")

    actionizer.play_album.assert_called_once_with("Haken", "The Mountain")
