# Day 15 - LangGraph Agent with Tool Calling

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool

llm = ChatCohere(
    cohere_api_key="cohere_uqewmYGinVgU2UhnWe0jtLLzr0gnFXtgWrpmZR810tRS9u",
    model="command-r-plus-08-2024"
)
def get_text(response):
    if isinstance(response.content, list):
        for block in response.content:
            if isinstance(block, dict) and block.get('type') == 'text':
                return block['text']
    return response.content

# TOOLS
# @tool decorator turns a Python function into an AI tool
# the docstring tells the AI what the tool does
# the AI reads the docstring to decide when to use it
@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression. 
    Use this for any math calculation.
    Example: '2 + 2', '10 * 5', '100 / 4'"""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except:
        return "Error: Invalid expression"

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city.
    Use this when user asks about weather."""
    # fake weather data - in real app this calls a weather API
    weather_data = {
        "lahore": "Hot and sunny, 38°C",
        "karachi": "Humid, 35°C",
        "islamabad": "Partly cloudy, 32°C"
    }
    return weather_data.get(city.lower(), f"Weather data not available for {city}")

@tool
def word_counter(text: str) -> str:
    """Count the number of words in a text.
    Use this when user wants to count words."""
    count = len(text.split())
    return f"Word count: {count} words"

# list of all tools
tools = [calculator, get_weather, word_counter]
# bind tools to llm
# this tells the AI which tools exist and what they do
llm_with_tools = llm.bind_tools(tools)

# STATE 
class State(TypedDict):
    messages: Annotated[list, add_messages]

# NODES
def agent_node(state: State):
    # AI decides: answer directly OR call a tool
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

# GRAPH
# ToolNode runs whatever tool AI requested
# tools_condition checks if AI wants a tool or is done
# if tool needed: go to tools node
# if done: go to END
# after tool runs: always go back to agent
# this creates the loop
graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")

memory = MemorySaver()
app = graph.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "faiq"}}

# RUN - interactive chat
# watch how AI automatically picks the right tool
print("AI Agent with Tools")
print("Try: math questions, weather, word counting")
print("Type 'quit' to exit\n")

first_message = True
behavior = input("Set AI behavior (or press Enter to skip): ")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    if first_message and behavior:
        messages = [
            SystemMessage(content=behavior),
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