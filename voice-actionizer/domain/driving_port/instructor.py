import os
import uuid
from abc import ABC, abstractmethod

from langfuse.callback import CallbackHandler

from domain.driven_port.actionizer import Actionizer
from domain.driven_port.answerer import Answerer
from domain.driving_port.graph import get_graph


langfuse_handler = CallbackHandler(
    public_key=os.environ.get("LANGFUSE_INIT_PROJECT_PUBLIC_KEY"),
    secret_key=os.environ.get("LANGFUSE_INIT_PROJECT_SECRET_KEY"),
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
