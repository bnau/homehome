import pyttsx3

from domain.driven_port.answerer import Answerer

engine = None


def _get_engine():
    global engine
    if engine is None:
        try:
            engine = pyttsx3.init()
            engine.setProperty('voice', 'fr')
            engine.setProperty('rate', 150)
        except Exception as e:
            print(e)
            engine = None
    return engine


class Tts(Answerer):
    def answer(self, message: str):
        engine = _get_engine()
        engine.say(message)
        engine.runAndWait()
        engine.stop()
