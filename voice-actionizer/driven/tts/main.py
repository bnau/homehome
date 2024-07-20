import pyttsx3

from domain.driven_port.answerer import Answerer

engine = None

def _get_engine():
    global engine
    if engine is None:
        try:
            engine = pyttsx3.init()
            print(engine.getProperty('voices'))
            voice = engine.getProperty('voices')[0]
            engine.setProperty('voice', 'french')
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
