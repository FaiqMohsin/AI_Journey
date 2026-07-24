# Day 16 - ChromaDB Vector Database

import chromadb

# SETUP - PersistentClient saves data to disk between runs
client = chromadb.PersistentClient(path="./chroma_db")

# delete if exists to start fresh
try:
    client.delete_collection("knowledge_base")
except:
    pass

# CREATE COLLECTION AND ADD DOCUMENTS
# collection = table in a database, metadata = extra info for filtering
# ChromaDB automatically converts text to embeddings
collection = client.create_collection("knowledge_base")

collection.add(
    documents=[
        "Python is a high level programming language known for simplicity.",
        "LangChain is a framework for building LLM powered applications.",
        "LangGraph is used for building stateful AI agents with loops.",
        "ChromaDB is an open source vector database for AI applications.",
        "RAG stands for Retrieval Augmented Generation.",
        "FastAPI is a modern Python framework for building REST APIs.",
        "Docker is used to containerize applications for deployment.",
        "Vector databases store embeddings and allow semantic search.",
        "AI agents can use tools to take actions in the real world."
    ],
    metadatas=[
        {"topic": "python"},
        {"topic": "langchain"},
        {"topic": "langgraph"},
        {"topic": "chromadb"},
        {"topic": "rag"},
        {"topic": "fastapi"},
        {"topic": "docker"},
        {"topic": "vectordb"},
        {"topic": "agents"}
    ],
    ids=["doc1", "doc2", "doc3", "doc4", "doc5",
         "doc6", "doc7", "doc8", "doc9"]
)
print(f"Collection ready with {collection.count()} documents\n")

# INTERACTIVE SEARCH
# user types query, ChromaDB finds most semantically similar documents
# distance = how similar - lower is better, where = filter by metadata
print("ChromaDB Semantic Search")
print("Commands: type any query, or 'filter:<topic>' to filter")
print("Example: 'filter:python' then search")
print("Type 'quit' to exit\n")

active_filter = None

while True:
    user_input = input("Search: ")

    if user_input.lower() == "quit":
        break

    # check if user wants to filter by topic
    if user_input.startswith("filter:"):
        active_filter = user_input.split(":")[1].strip()
        print(f"Filter set to: {active_filter}\n")
        continue

    # build query
    query_params = {
        "query_texts": [user_input],
        "n_results": 3
    }

    # apply filter if set
    if active_filter:
        query_params["where"] = {"topic": active_filter}

    results = collection.query(**query_params)

    print("Most relevant results:")
    for doc, distance in zip(results["documents"][0], results["distances"][0]):
        print(f"  [{distance:.3f}] {doc}")
    print()