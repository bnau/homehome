from dependency_injector import containers, providers

from actions.driven.home_server.main import HomeServer
from actions.driven.inmemory.server import InMemoryServer
from actions.driving_port.book_reader import DomainBookReader
from actions.driving_port.music_player import DomainMusicPlayer
from ner.driven.actions.main import MainActionizer
from ner.driven.inmemory.metadata_retriever import InMemoryMetadataRetriever
from ner.driven.inmemory.answerer import InMemoryAnswerer
from ner.driven.tts.main import Tts
from ner.driving_port.instructor import DomainInstructor


class RealLifeActions(containers.DeclarativeContainer):
    server = providers.Singleton(HomeServer)
    book_reader = providers.Factory(DomainBookReader, server=server)
    music_player = providers.Factory(DomainMusicPlayer, server=server)


class InMemoryActions(containers.DeclarativeContainer):
    server = providers.Singleton(InMemoryServer)
    book_reader = providers.Factory(DomainBookReader, server=server)
    music_player = providers.Factory(DomainMusicPlayer, server=server)


class InMemory(containers.DeclarativeContainer):
    answerer = providers.Singleton(InMemoryAnswerer)
    metadata_retriever = providers.Singleton(InMemoryMetadataRetriever)


class RealLife(containers.DeclarativeContainer):
    answerer = providers.Singleton(Tts)
    metadata_retriever = providers.Singleton(InMemoryMetadataRetriever)


class Domain(containers.DeclarativeContainer):
    driven = providers.DependenciesContainer()
    actions = providers.DependenciesContainer()

    actionizer = providers.Factory(
        MainActionizer,
        book_reader=actions.book_reader,
        music_player=actions.music_player
    )

    instructor = providers.Factory(
        DomainInstructor,
        actionizer=actionizer,
        answerer=driven.answerer,
        metadata_retriever=driven.metadata_retriever
    )


class Cli(containers.DeclarativeContainer):
    driven = providers.Container(InMemory)
    actions = providers.Container(InMemoryActions)

    domain = providers.Container(Domain, driven=driven, actions=actions)


class Device(containers.DeclarativeContainer):
    driven = providers.Container(RealLife)
    actions = providers.Container(RealLifeActions)

    domain = providers.Container(Domain, driven=driven, actions=actions)
