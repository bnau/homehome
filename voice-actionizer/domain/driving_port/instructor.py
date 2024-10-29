from abc import ABC, abstractmethod
from typing import Union, Optional, Any

from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import PydanticOutputParser, BaseOutputParser
from langchain_core.output_parsers.base import T
from langchain_core.runnables import RunnableConfig

from domain.driven_port.actionizer import Actionizer
from domain.driven_port.answerer import Answerer
from domain.model.intention import IntentionFactory
from langchain.chains import RetrievalQA
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_core.documents import Document

from langchain_experimental.llms.ollama_functions import OllamaFunctions

from langfuse.callback import CallbackHandler
from langchain_milvus import Milvus
from langchain_ollama import OllamaEmbeddings
from langchain_community.llms import Ollama

langfuse_handler = CallbackHandler(
    public_key="pk-lf-3231235e-46b0-431d-9795-7d256ea27195",
    secret_key="sk-lf-0195c5f1-f370-4e87-8394-cfc604773ab8",
    host="http://localhost:3000"
)

# The easiest way is to use Milvus Lite where everything is stored in a local file.
# If you have a Milvus server you can use the server URI such as "http://localhost:19530".
URI = "./milvus_example.db"

embeddings = OllamaEmbeddings(
    model="stablelm2",
)

vector_store = Milvus(
    embedding_function=embeddings,

    connection_args={"uri": URI},
)

vector_store.add_documents([
    Document(
        page_content="l'attribut intention est l'une des valeurs suivantes en minuscule: readBook, playMusic.",
    ),
    Document(
        page_content="l'attribut author est l'une des valeurs suivantes: Tolkien, Rowling.",
    ),
], ids=["intention", "author"])


class IgnoreParser(BaseOutputParser):
    def parse(self, response):
        return response

    def invoke(
            self,
            input: Union[str, BaseMessage],
            config: Optional[RunnableConfig] = None,
            **kwargs: Any,
    ) -> T:
        return input


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
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                 """
                 Tu es un expert en extraction d'informations.
                                                    
                 Extraits uniquement les informations pertinentes du texte.
                 Si tu ne connais pas la valeur d'un attribut, il n'a pas de valeur.
                 Les attributs à extraire sont: intention, author, title.
                 
                 La réponse est de la forme:
                 {{
                     "tool": "IntentionFactory",
                     "tool_input": {{
                         ...
                     }}
                 }}
                 
                 
                 Context: {context}
                 """),
                ("human", "{input}"),
            ]
        )
        parser = IgnoreParser()
        question_answer_chain = create_stuff_documents_chain(self.llm.with_structured_output(schema=IntentionFactory),
                                                             prompt,
                                                             output_parser=parser)
        runnable = create_retrieval_chain(vector_store.as_retriever(), question_answer_chain)
        intent = runnable.invoke({"input": command}, config={"callbacks": [langfuse_handler]})['answer']
        intent.create_intention(self.actionizer, self.answerer).actionize()
