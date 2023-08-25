import asyncio
import time

from rasa.model import get_latest_model
from rasa.core.agent import Agent
from tts.main import say
from rasa.utils.endpoints import EndpointConfig
from vosk import Model, KaldiRecognizer
import pyaudio

nlu_model = get_latest_model("chatbot/models")
agent = Agent.load(model_path=nlu_model, action_endpoint=EndpointConfig(url="http://localhost:3000"))

vosk_model = Model(r"stt/model")
recognizer_limited = KaldiRecognizer(vosk_model, 16000,
                                     '["switch audio", "bonjour", "lis un livre de chateaubriand", "annuler"]')
recognizer = KaldiRecognizer(vosk_model, 16000)

previous_text = ""
text = ""

def process_audio(data, _frame_count, _time_info, _status):
    global previous_text
    if previous_text == "bonjour":
        if recognizer_limited.AcceptWaveform(data):
            text = recognizer_limited.Result()[14:-3]
            print(f"' {text} '")
            if text != '':
                previous_text = text
                result = asyncio.run(agent.handle_text(text))
                if len(result) > 0:
                    say(result[0]['text'])
    elif recognizer.AcceptWaveform(data):
        text = recognizer.Result()[14:-3]
        print(f"' {text} '")

        if text != '':
            previous_text = text
    return (data, pyaudio.paContinue)

mic=None
stream=None
while True:
    try:
        if mic is None:
            mic = pyaudio.PyAudio()
        if stream is None:
            stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192, stream_callback=process_audio)
        if not stream.is_active() or stream.is_stopped():
            raise Exception("stream dead")
    except Exception as e:
        print(e)
        try:
            mic.terminate()
            stream.stop_stream()
            stream.close()
        except:
            pass
        stream = None
        mic = None
    time.sleep(.1)
