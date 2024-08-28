from abc import ABC, abstractmethod

from domain.driven_port.actionizer import Actionizer
from domain.driven_port.answerer import Answerer
from domain.model.intention import IntentionFactory

from langchain_core.prompts import PromptTemplate

from langchain_experimental.llms.ollama_functions import OllamaFunctions


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
        self.llm = OllamaFunctions(model="phi3", format="json", temperature=-1)


    def instruct(self, command: str):
        prompt = PromptTemplate.from_template(
                    """Tu es un expert en extraction d'informations.
                    Réponds exactement le même texte que l'utilisateur.
                    Extraits uniquement les informations pertinentes du texte.
                    Si tu ne connais pas la valeur d'un attribut demandé à extraire,
                    retourne null pour la valeur de l'attribut.
                    action peut contenir les valeurs suivantes: read_book, play_album, none
                    author est présent dans la question.
                    
                    Human: {question}
                    AI: """
        )

        runnable = prompt | self.llm.with_structured_output(schema=IntentionFactory)
        intent = runnable.invoke(command)
        intent.create_intention(self.actionizer, self.answerer).actionize()
