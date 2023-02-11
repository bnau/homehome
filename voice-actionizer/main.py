import asyncio
from rasa.model import get_latest_model
from rasa.core.agent import Agent
from tts.main import say
from rasa.utils.endpoints import EndpointConfig
from vosk import Model, KaldiRecognizer
import pyaudio

nlu_model = get_latest_model("chatbot/models")
agent = Agent.load(model_path=nlu_model, action_endpoint=EndpointConfig(url="http://localhost:3000"))

vosk_model = Model(r"stt/model_old")
recognizer = KaldiRecognizer(vosk_model, 16000,
'["dark side of the moon", "wish you were here", "dream theater", "bonjour", "lis un livre de chateaubriand"]')

mic = pyaudio.PyAudio()
stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

previous_text = ""



while True:
    data = stream.read(4096, exception_on_overflow=False)

    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()[14:-3]
        print(f"' {text} '")
        if previous_text == "bonjour" and text != '':
            result = asyncio.run(agent.handle_text(text))
            if len(result) > 0:
                say(result[0]['text'])

        if text != '':
            previous_text = text
