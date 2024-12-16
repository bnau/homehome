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

from domain.driven_port.metadata_retriever import MetadataRetriever
from domain.driving_port.db import add_document, get_db
from domain.model.intention import IntentionFactory


def init_db_chain(state, config):
    metadata_retriever: MetadataRetriever = config["configurable"].get("metadataRetriever")
    for album in metadata_retriever.get_albums():
        add_document(f"\"{album.title}\" is the title of an album by the artist \"{album.artist}\".")

    add_document("\"Tolkien\" is a book author")

    return state


llm = OllamaFunctions(model="llama3.2", format="json")
db = get_db()


def chat_chain(state, config):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system",
             """
             You are an expert in information extraction.
             
             You are given a text that contains information about a book or an album.
             The text is in French, but don’t translate the extracted information.
             
             If you don’t find an attribute, leave it empty.
             
             The attributes to extract are: author, title, artist.
             There is an additional attribute called intention, which can be either readBook or playAlbum.
             tool is always IntentionFactory.
             tool is not intention, as tool is always IntentionFactory.
             
             La réponse est de la forme:
             {{
                 "tool": "IntentionFactory",
                 "tool_input": {{
                    "intention": ...
                    "author": ...
                    "title": ...
                    "artist": ...
                 }}
             }}
             
             
             Context: {context}
             """),
            ("human", "{input}"),
        ]
    )
    runnable = prompt | llm.with_structured_output(schema=IntentionFactory)

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
