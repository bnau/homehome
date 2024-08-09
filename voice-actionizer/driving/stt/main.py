import numpy as np

from driven.tts.main import Tts
from vosk import Model, KaldiRecognizer
import soundcard as sc

vosk_model = Model("driving/stt/model")
rate = 48000
recognizer_limited = KaldiRecognizer(vosk_model, rate,
                                     '["switch audio", "bonjour", "lis un livre de chateaubriand", "annuler"]')
recognizer = KaldiRecognizer(vosk_model, rate)

previous_text = ""
text = ""

tts = Tts()

def process_audio(data):
    global previous_text
    if previous_text == "bonjour":
        if recognizer_limited.AcceptWaveform(data):
            text = recognizer_limited.Result()[14:-3]
            print(f"' {text} '")
            if text != '':
                previous_text = text
                result = [{text: text}]
                if len(result) > 0:
                    tts.answer(result[0]['text'])
    elif recognizer.AcceptWaveform(data):
        text = recognizer.Result()[14:-3]
        print(f"' {text} '")

        if text != '':
            previous_text = text

mic=None
rec_sec = 2
while True:
    try:
        if mic is None:
            mic = sc.default_microphone()
        data = mic.record(samplerate=rate, numframes=rate*rec_sec)
        process_audio(np.int16(data / np.max(np.abs(data)) * 32767).tobytes())
    except Exception as e:
        print(e)
        mic = None

