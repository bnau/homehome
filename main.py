import asyncio
from rasa.model import get_latest_model
from rasa.core.agent import Agent
from tts.main import say


def load_interpreter(model_path):
    nlu_model = get_latest_model(model_path)
    return Agent.load(nlu_model)


agent = load_interpreter("chatbot/models")

result = asyncio.run(agent.handle_text("Hello"))

say(result[0]['text'])

result = asyncio.run(agent.handle_text("Non, ça va pas trop"))

say(result[0]['text'])
