#Day 18 - Agentic RAG with Langgraph

import os
import chromadb
import cohere
from chromadb.utils import embedding_functions
from pypdf import PdfReader
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langchain_cohere import ChatCohere
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool

# SETUP
# two models:
# cohere_client - for direct API calls in RAG tool
# llm - LangChain wrapper for LangGraph agent
# command-r-plus-08-2024 required for tool calling
API_KEY= "cohere_uqewmYGinVgU2UhnWe0jtLLzr0gnFXtgWrpmZR810tRS9u"
cohere_client=cohere.ClientV2(api_key=API_KEY)
cohere_ef=embedding_functions.CohereEmbeddingFunction(
    api_key=API_KEY, model_name = "embed-v4.0")
llm =ChatCohere(cohere_api_key= API_KEY, model="command-r-plus-08-2024")

# CHROMADB - persistent, loads existing data
chroma_client= chromadb.PersistentClient(path="/rag.db")
existing=[c.name for c in chroma_client.list_collections()]
if "rag_docs" in existing:
    collection = chroma_client.get_collection("rag_docs", embedding_function=cohere_ef)
    print(f"Loaded existing database: {collection.count()} chunks\n")
else:
    collection = chroma_client.create_collection("rag_docs", embedding_function=cohere_ef)
    print("New database created.\n")

# PDF INDEXING - load → chunk → store in ChromaDB  
def index_pdf(file_path: str):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}\n")
        return

    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    if not text.strip():
        print("No text extracted.\n")
        return

    chunks, start = [], 0
    while start < len(text):
        chunk = text[start:start + 500].strip()
        if chunk:
            chunks.append(chunk)
        start += 450

    offset = collection.count()
    collection.add(
        documents=chunks,
        metadatas=[{"source": os.path.basename(file_path)} for _ in chunks],
        ids=[f"chunk_{offset + i}" for i in range(len(chunks))]
    )
    print(f"Indexed {len(chunks)} chunks. Total: {collection.count()}\n")

# RAG AS A TOOL - @tool turns this function into tool for agent to call
# docstring tells the agent WHEN to use this tool
# agent reads the docstring and decides automatically 
@tool
def search_documents(query: str) -> str:
    """Search indexed documents for relevant information.
    Use this when the user asks about history, events, or facts
    that would be found in the loaded documents."""
    print("🔍 Searching documents...")
    if collection.count() == 0:
        return "No documents loaded. Ask user to add a PDF first."

    results = collection.query(
        query_texts=[query],
        n_results=min(3, collection.count())
    )

    chunks = results["documents"][0]
    sources = list(set(m["source"] for m in results["metadatas"][0]))
    context = "\n\n".join(chunks)

    # generate answer from retrieved context
    prompt = f"""Answer using ONLY the context below.
If not found say "I don't have that information in the documents."

Context:
{context}

Question: {query}
Answer:"""

    response = cohere_client.chat(
        model="command-a-plus-05-2026",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = ""
    for block in response.message.content:
        if hasattr(block, 'text'):
            answer = block.text
            break

    return f"{answer}\n\nSource: {', '.join(sources)}"

# LANGGRAPH AGENT - decides: answer directly OR call search_documents 
tools = [search_documents]
llm_with_tools = llm.bind_tools(tools)

class State(TypedDict):
    messages: Annotated[list, add_messages]

def agent_node(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

graph = StateGraph(State)
graph.add_node("agent", agent_node)
graph.add_node("tools", ToolNode(tools))
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")

memory = MemorySaver()
app = graph.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "faiq_rag"}}

# RESPONSE HELPER
# extracts text from LangGraph response
# handles both string and list content
def get_response(result):
    last = result["messages"][-1]
    if isinstance(last.content, list):
        for block in last.content:
            if isinstance(block, dict) and block.get("type") == "text":
                return block["text"]
    return last.content

# MAIN LOOP
print("Agentic RAG System")
print("add <filepath> — load a PDF")
print("quit           — exit")
print("anything else  — ask a question\n")

first_message = True

while True:
    user_input = input("You: ").strip()

    if not user_input:
        continue

    elif user_input.lower() == "quit":
        print("Goodbye!")
        break

    elif user_input.lower().startswith("add "):
        index_pdf(user_input[4:].strip())

    else:
        if first_message:
            messages = [
                SystemMessage(content="You are a helpful assistant with access to document search. Use the search_documents tool when asked about historical events or document content. Answer general questions directly."),
                HumanMessage(content=user_input)
            ]
            first_message = False
        else:
            messages = [HumanMessage(content=user_input)]

        result = app.invoke({"messages": messages}, config=config)
        print(f"AI: {get_response(result)}\n")