import pyttsx3

engine = None

def _get_engine():
    global engine
    if engine is None:
        try:
            engine = pyttsx3.init()
        except Exception as e:
            print(e)
            engine = None
    return engine


def say(message):
    engine = _get_engine()
    if engine is None:
        return
    engine.say(message)
    engine.runAndWait()
    engine.stop()
