import sys

from dependency_injector.wiring import inject, Provide

from di.containers import Chat
from ner.driving_port.instructor import Instructor


@inject
def main(
        entrypoint: Instructor = Provide[Chat.domain.instructor],
):
    while True:
        command = input('--> ')
        entrypoint.instruct(command)


if __name__ == '__main__':
    application = Chat()
    application.wire(modules=[__name__])
    main(*sys.argv[1:])
