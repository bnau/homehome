from domain.instructor import Instructor
from driven.inmemory.actionizer import InMemoryActionizer
from driven.inmemory.answerer import InMemoryAnswerer
from driven.tts.main import Tts

actionizer = InMemoryActionizer()
answerer = Tts()

entrypoint = Instructor(actionizer, answerer)

def main():
    while True:
        command = input('--> ')
        entrypoint.instruct(command)

if __name__ == '__main__':
    main()