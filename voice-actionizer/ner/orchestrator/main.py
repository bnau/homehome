import os
import uuid
from typing import Any

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langfuse.callback import CallbackHandler
from langgraph.checkpoint.memory import MemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from typing_extensions import TypedDict

from ner.driven_port.metadata_retriever import MetadataRetriever
from ner.model.intention import IntentionFactory


class Orchestrator:
    def __init__(self, metadata_retriever: MetadataRetriever, store):
        self.__metadata_retriever = metadata_retriever
        self.__store = store
        self.__llm = ChatOllama(model="homehome", temperature=0)
        self.__langfuse_handler = CallbackHandler(
                   public_key=os.environ.get("LANGFUSE_INIT_PROJECT_PUBLIC_KEY"),
                   secret_key=os.environ.get("LANGFUSE_INIT_PROJECT_SECRET_KEY"),
                   host="http://localhost:3000"
               )

        def init_db_chain(state, config):
            metadata_retriever: MetadataRetriever = config["configurable"].get("metadata_retriever")
            for album in metadata_retriever.get_albums():
                self.__store.add(f"\"{album.title}\" is the title of an album by the artist \"{album.artist}\".")

            self.__store.add('"Mémoires d\'Outre-Tombe" is a book by the author "Chateaubriand"')

            return state

        def chat_chain(state, config):
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("assistant", "{context}"),
                    ("human", "{input}"),
                ]
            )
            parser = PydanticOutputParser(pydantic_object=IntentionFactory)
            runnable = prompt | self.__llm | parser

            vectors = self.__store.retrieve(state["messages"][-1])

            response = runnable.invoke({"input": state["messages"][-1], "context": vectors}, config=config)
            return {"messages": [response]}

        class State(TypedDict):
            messages: Any
            db: Any

        workflow = StateGraph(State)
        workflow.add_node("init_db", init_db_chain)
        workflow.add_node("chat", chat_chain)

        workflow.add_edge(START, "init_db")
        workflow.add_edge("init_db", "chat")
        workflow.add_edge("chat", END)

        self.__graph = workflow.compile(checkpointer=MemorySaver())

    def invoke(self, command: str) -> IntentionFactory:
        return self.__graph.invoke(
            {"messages": [command]},
            config={"configurable": {"thread_id": str(uuid.uuid4()), "metadata_retriever": self.__metadata_retriever},
                    "callbacks": [self.__langfuse_handler]}).get('messages')[-1]
