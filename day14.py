# Day 14 - LangGraph Basics

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatCohere(
    cohere_api_key="cohere_uqewmYGinVgU2UhnWe0jtLLzr0gnFXtgWrpmZR810tRS9u",
    model="command-a-plus-05-2026"
)

def get_text(response):
    if isinstance(response.content, list):
        for block in response.content:
            if isinstance(block, dict) and block.get('type') == 'text':
                return block['text']
    return response.content 

# STATE
# TypedDict = dictionary with defined types
# add_messages = special reducer
# appends new messages instead of replacing
# this is how conversation history builds up
class State (TypedDict):
    messages: Annotated[list, add_messages]

# NODE
# Plain Python function, receives current state, returns what to update in state
def call_llm(state:State):
    response= llm.invoke(state["messages"])
    return {"messages":[response]}

# GRAPH - add nodes, connect with edges, compile
graph = StateGraph(State)
graph.add_node("llm", call_llm)
graph.add_edge(START,"llm")
graph.add_edge("llm", END)
memory = MemorySaver()
app = graph.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "faiq"}}

# USER CHAT
# combine everything into interactive chat
# user types, LangGraph handles memory automatically
print("\n3 - Interactive Chat with Memory")
print("Type 'quit' to exit\n")

ai_behavior = input("Program your response: ")

first_message = True

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Goodbye")
        break

    # first message includes system behavior
    # after that only human messages
    if first_message:
        messages = [
            SystemMessage(content=ai_behavior),
            HumanMessage(content=user_input)
        ]
        first_message = False
    else:
        messages = [HumanMessage(content=user_input)]

    result = app.invoke(
        {"messages": messages},
        config=config
    )
    print(f"AI: {get_text(result['messages'][-1])}\n")