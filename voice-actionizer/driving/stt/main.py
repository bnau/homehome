import sys

import numpy as np
from dependency_injector.wiring import Provide, inject

from vosk import Model, KaldiRecognizer
import soundcard as sc

from domain.driving_port.instructor import Instructor
from ext.containers import Device

vosk_model = Model("driving/stt/model")
rate = 48000
recognizer_limited = KaldiRecognizer(vosk_model, rate,
                                     '["switch audio", "bonjour", "lis un livre de chateaubriand", "annuler"]')
recognizer = KaldiRecognizer(vosk_model, rate)

previous_text = ""
text = ""


def process_audio(entrypoint: Instructor, data):
    global previous_text
    if previous_text == "bonjour":
        if recognizer_limited.AcceptWaveform(data):
            text = recognizer_limited.Result()[14:-3]
            print(f"' {text} '")
            if text != '':
                previous_text = text
                entrypoint.instruct(text)
    elif recognizer.AcceptWaveform(data):
        text = recognizer.Result()[14:-3]
        print(f"' {text} '")

        if text != '':
            previous_text = text


@inject
def main(
        entrypoint: Instructor = Provide[Device.domain.instructor],
):
    mic=None
    rec_sec = 2

    while True:
        try:
            if mic is None:
                mic = sc.default_microphone()
            data = mic.record(samplerate=rate, numframes=rate*rec_sec)
            process_audio(entrypoint, np.int16(data / np.max(np.abs(data)) * 32767).tobytes())
        except Exception as e:
            print(e)
            mic = None


if __name__ == '__main__':
    application = Device()
    application.wire(modules=[__name__])
    main(*sys.argv[1:])
