import os
import uuid
from typing import Union, Optional, Any

from langfuse.callback import CallbackHandler

from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import BaseOutputParser, PydanticOutputParser
from langchain_core.output_parsers.base import T
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

from ner.driven_port.metadata_retriever import MetadataRetriever
from ner.orchestrator.db import add_document, get_db
from langchain_ollama import ChatOllama

from ner.model.intention import IntentionFactory


def init_db_chain(state, config):
    metadata_retriever: MetadataRetriever = config["configurable"].get("metadata_retriever")
    for album in metadata_retriever.get_albums():
        add_document(f"\"{album.title}\" is the title of an album by the artist \"{album.artist}\".")

    add_document("\"Chateaubriand\" is a book author")

    return state


langfuse_handler = CallbackHandler(
    public_key=os.environ.get("LANGFUSE_INIT_PROJECT_PUBLIC_KEY"),
    secret_key=os.environ.get("LANGFUSE_INIT_PROJECT_SECRET_KEY"),
    host="http://localhost:3000"
)

llm = ChatOllama(model="homehome", temperature=0)
db = get_db()


def chat_chain(state, config):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("assistant", "{context}"),
            ("human", "{input}"),
        ]
    )
    parser = PydanticOutputParser(pydantic_object=IntentionFactory)
    runnable = prompt | llm | parser

    vectors = db.similarity_search(state["messages"][-1])

    response = runnable.invoke({"input": state["messages"][-1], "context": vectors}, config=config)
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


def invoke_graph(command: str, metadata_retriever: MetadataRetriever) -> IntentionFactory:
    return get_graph().invoke(
        {"messages": [command]},
        config={"configurable": {"thread_id": str(uuid.uuid4()), "metadata_retriever": metadata_retriever},
                "callbacks": [langfuse_handler]}).get('messages')[-1]
