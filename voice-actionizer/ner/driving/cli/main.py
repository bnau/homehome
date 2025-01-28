import sys

from dependency_injector.wiring import inject, Provide

from di.containers import Device
from ner.driving_port.command import Command


@inject
def main(
        arg: str,
        command: Command = Provide[Device.domain.command]
):
    command.launch(arg)


if __name__ == '__main__':
    application = Device()
    application.wire(modules=[__name__])
    main(*sys.argv[1:])
