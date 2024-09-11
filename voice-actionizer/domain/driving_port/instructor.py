from abc import ABC, abstractmethod

from domain.driven_port.actionizer import Actionizer
from domain.driven_port.answerer import Answerer
from domain.model.intention import IntentionFactory

from langchain_core.prompts import PromptTemplate

from langchain_core.tools import tool
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
        self.llm = OllamaFunctions(model="stablelm2", format="json", temperature=1000)


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
        intent = runnable.invoke(command)
        intent.create_intention(self.actionizer, self.answerer).actionize()
