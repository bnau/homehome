import sys

from dependency_injector.wiring import inject, Provide

from ext.containers import Cli
from domain.driving_port.instructor import Instructor


@inject
def main(
        entrypoint: Instructor = Provide[Cli.domain.instructor],
):
    while True:
        command = input('--> ')
        entrypoint.instruct(command)


if __name__ == '__main__':
    application = Cli()
    application.wire(modules=[__name__])
    main(*sys.argv[1:])
