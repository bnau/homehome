import asyncio
from rasa.model import get_latest_model
from rasa.core.agent import Agent
from tts.main import say
from rasa.utils.endpoints import EndpointConfig


def load_interpreter(model_path):
    nlu_model = get_latest_model(model_path)
    return Agent.load(model_path=nlu_model, action_endpoint=EndpointConfig(url="http://localhost:5055"))


agent = load_interpreter("chatbot/models")

result = asyncio.run(agent.handle_text("lis un livre de Chateaubriand"))

say(result[0]['text'])
