from dependency_injector import containers, providers

from domain.driving_port.instructor import DomainInstructor
from driven.inmemory.actionizer import InMemoryActionizer
from driven.inmemory.answerer import InMemoryAnswerer
from driven.action_server.main import ServerActionizer
from driven.tts.main import Tts


class InMemory(containers.DeclarativeContainer):
    actionizer = providers.Singleton(InMemoryActionizer)
    answerer = providers.Singleton(InMemoryAnswerer)


class RealLife(containers.DeclarativeContainer):
    actionizer = providers.Singleton(ServerActionizer)
    answerer = providers.Singleton(Tts)


class Domain(containers.DeclarativeContainer):
    driven = providers.DependenciesContainer()

    instructor = providers.Factory(
        DomainInstructor,
        actionizer=driven.actionizer,
        answerer=driven.answerer
    )


class Cli(containers.DeclarativeContainer):
    driven = providers.Container(InMemory)

    domain = providers.Container(Domain, driven=driven)


class Device(containers.DeclarativeContainer):
    driven = providers.Container(RealLife)

    domain = providers.Container(Domain, driven=driven)