import os
import time
import numpy as np

from tts.main import say
from vosk import Model, KaldiRecognizer
import soundcard as sc
import wave
from scipy.io.wavfile import write

vosk_model = Model(r"stt/model")
rate = 48000
recognizer_limited = KaldiRecognizer(vosk_model, rate,
                                     '["switch audio", "bonjour", "lis un livre de chateaubriand", "annuler"]')
recognizer = KaldiRecognizer(vosk_model, rate)

previous_text = ""
text = ""

def process_audio(data):
    global previous_text
    if previous_text == "bonjour":
        if recognizer_limited.AcceptWaveform(data):
            text = recognizer_limited.Result()[14:-3]
            print(f"' {text} '")
            if text != '':
                previous_text = text
                if "livre" in text:
                    say('ok')
    elif recognizer.AcceptWaveform(data):
        text = recognizer.Result()[14:-3]
        print(f"' {text} '")

        if text != '':
            previous_text = text

mic=None
stream=None
rec_sec = 2
while True:
    # try:
        if mic is None:
            mic = sc.default_microphone()
        if stream is None:
            data = mic.record(samplerate=rate, numframes=rate*rec_sec)
            write('recorded.wav',rate,np.int16(data / np.max(np.abs(data)) * 32767))
            with wave.open('recorded.wav', 'rb') as f:
                process_audio(f.readframes(rate*rec_sec))
    # if not stream.is_active() or stream.is_stopped():
    #         raise Exception("stream dead")
    # except Exception as e:
    #     print(e)
    #     # try:
    #     #     mic.terminate()
    #     #     stream.stop_stream()
    #     #     stream.close()
    #     # except:
    #     #     pass
    #     stream = None
    #     mic = None
    # time.sleep(.1)
