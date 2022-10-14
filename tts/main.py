import pyttsx3

engine = pyttsx3.init()


def say(message):
    engine.say(message)
    engine.runAndWait()
    engine.stop()
