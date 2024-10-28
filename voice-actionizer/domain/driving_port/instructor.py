from abc import ABC, abstractmethod

from domain.driven_port.actionizer import Actionizer
from domain.driven_port.answerer import Answerer
from domain.model.intention import IntentionFactory

from langchain_core.prompts import PromptTemplate

from langchain_core.tools import tool
from langchain_experimental.llms.ollama_functions import OllamaFunctions

from langfuse.callback import CallbackHandler
langfuse_handler = CallbackHandler(
    public_key="pk-lf-3231235e-46b0-431d-9795-7d256ea27195",
    secret_key="sk-lf-0195c5f1-f370-4e87-8394-cfc604773ab8",
    host="http://localhost:3000"
)

class Instructor(ABC):
    @abstractmethod
    def instruct(self, command: str):
        pass


class DomainInstructor:
    actionizer: Actionizer
    answerer: Answerer

    llm: OllamaFunctions

    def __init__(self, actionizer: Actionizer, answerer: Answerer):
        self.actionizer = actionizer
        self.answerer = answerer
        self.llm = OllamaFunctions(model="stablelm2", format="json")


    def instruct(self, command: str):
        prompt = PromptTemplate.from_template(
                    """Tu es un expert en extraction d'informations.
                    
                    Extraits uniquement les informations pertinentes du texte.
                    Si tu ne connais pas la valeur d'un attribut, il n'a pas de valeur.
                    tool==IntentionFactory.
                    Les attributs à extraire sont: action, author, title.
                    l'attribut action est l'une des valeurs suivantes en minuscule: readBook, playMusic.
                    l'attribut author est l'une des valeurs suivantes: Tolkien, Rowling.
                    
                    Voici la demande: {question}
                    AI: """
        )

        runnable = prompt | self.llm.with_structured_output(schema=IntentionFactory)
        intent = runnable.invoke(command, config={"callbacks": [langfuse_handler]})
        intent.create_intention(self.actionizer, self.answerer).actionize()
