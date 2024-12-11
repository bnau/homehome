from typing import Union, Optional, Any

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.output_parsers.base import T
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

from domain.driving_port.db import add_document, get_db
from domain.model.intention import IntentionFactory


def init_db_chain(state):
    add_document("l'attribut intention est l'une des valeurs suivantes en minuscule: readBook, playMusic.")
    add_document("l'attribut author est l'une des valeurs suivantes: Tolkien, Rowling.")
    return state

llm = OllamaFunctions(model="stablelm2", format="json")
db=get_db()


def chat_chain(state, config):
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
    question_answer_chain = create_stuff_documents_chain(llm.with_structured_output(schema=IntentionFactory),
                                                         prompt,
                                                         output_parser=IgnoreParser())
    runnable = create_retrieval_chain(db.as_retriever(), question_answer_chain)
    response = runnable.invoke({"input": state["messages"][-1]}, config=config)['answer']
    return {"messages": [response]}


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


class State(TypedDict):
    messages: Any
    db: Any


def get_graph():
    workflow = StateGraph(State)
    workflow.add_node("init_db", init_db_chain)
    workflow.add_node("chat", chat_chain)

    workflow.add_edge(START, "init_db")
    workflow.add_edge("init_db", "chat")
    workflow.add_edge("chat", END)
    return workflow.compile(checkpointer=MemorySaver())

