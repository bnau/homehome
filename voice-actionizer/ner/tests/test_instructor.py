import unittest.mock

from ner.driven_port.actionizer import Actionizer
from ner.driven_port.answerer import Answerer
from ner.driven.inmemory.metadata_retriever import InMemoryMetadataRetriever
from ner.driving_port.instructor import DomainInstructor


def test_instructor_should_call_actionizer():
    actionizer = unittest.mock.create_autospec(
        Actionizer, instance=True
    )
    answerer = unittest.mock.create_autospec(
        Answerer, instance=True
    )
    metadata_retriever = InMemoryMetadataRetriever()

    instructor = DomainInstructor(actionizer, answerer, metadata_retriever)
    instructor.instruct("Lis un livre de Chateaubriand")

    actionizer.read_book.assert_called_once_with("Chateaubriand")


def test_instructor_with_embedding():
    actionizer = unittest.mock.create_autospec(
        Actionizer, instance=True
    )
    answerer = unittest.mock.create_autospec(
        Answerer, instance=True
    )
    metadata_retriever = InMemoryMetadataRetriever()

    instructor = DomainInstructor(actionizer, answerer, metadata_retriever)
    instructor.instruct("Joue the mountain par haken")

    actionizer.play_album.assert_called_once_with("Haken", "The Mountain")
