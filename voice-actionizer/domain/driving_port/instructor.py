import uuid
from abc import ABC, abstractmethod

from langfuse.callback import CallbackHandler

from domain.driven_port.actionizer import Actionizer
from domain.driven_port.answerer import Answerer
from domain.driving_port.graph import get_graph

langfuse_handler = CallbackHandler(
    public_key="pk-lf-40c11769-fdf6-456c-b3c5-b6e6943db850",
    secret_key="sk-lf-6c8a87ca-f217-42ed-8cd3-01d05cb24833",
    host="http://localhost:3000"
)


class Instructor(ABC):
    @abstractmethod
    def instruct(self, command: str):
        pass


class DomainInstructor:
    actionizer: Actionizer
    answerer: Answerer

    def __init__(self, actionizer: Actionizer, answerer: Answerer):
        self.actionizer = actionizer
        self.answerer = answerer

    def instruct(self, command: str):
        intent = get_graph().invoke({"messages": [command]}, config={"configurable": {"thread_id": str(uuid.uuid4())},
                                                                     "callbacks": [langfuse_handler]}).get('messages')[
            -1]
        intent.create_intention(self.actionizer, self.answerer).actionize()
