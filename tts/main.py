import pyttsx3
import sys
engine = pyttsx3.init() # object creation

engine.say(sys.argv[1])
engine.runAndWait()
engine.stop()
