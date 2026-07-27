# Day 17 - RAG System with Real Documents

import chromadb
import cohere
import os
from chromadb.utils import embedding_functions
from pypdf import PdfReader

# ─────────────────────────────────────────
# SETUP
# ─────────────────────────────────────────
cohere_client = cohere.ClientV2(api_key="cohere_uqewmYGinVgU2UhnWe0jtLLzr0gnFXtgWrpmZR810tRS9u")

cohere_ef = embedding_functions.CohereEmbeddingFunction(
    api_key="cohere_uqewmYGinVgU2UhnWe0jtLLzr0gnFXtgWrpmZR810tRS9u",
    model_name="embed-v4.0"
)

chroma_client = chromadb.PersistentClient(path="./rag_db")

try:
    chroma_client.delete_collection("rag_docs")
except:
    pass

collection = chroma_client.create_collection(
    name="rag_docs",
    embedding_function=cohere_ef
)

# ─────────────────────────────────────────
# DOCUMENT LOADER
# supports PDF and TXT files
# chunks text into smaller pieces
# chunk_size = how many characters per chunk
# overlap = how many characters shared between chunks
# overlap prevents losing context at chunk boundaries
# ─────────────────────────────────────────
def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def load_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        if chunk.strip():
            chunks.append(chunk)
        start = end - overlap
    return chunks

def index_document(file_path: str):
    print(f"Loading: {file_path}")

    # load based on file type
    if file_path.endswith(".pdf"):
        text = load_pdf(file_path)
    elif file_path.endswith(".txt"):
        text = load_txt(file_path)
    else:
        print("Unsupported file type. Use PDF or TXT.")
        return

    # chunk the text
    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks from {file_path}")

    # get existing count to avoid duplicate IDs
    existing_count = collection.count()

    # add chunks to ChromaDB
    collection.add(
        documents=chunks,
        metadatas=[{"source": os.path.basename(file_path), "chunk": i}
                   for i in range(len(chunks))],
        ids=[f"doc_{existing_count + i}" for i in range(len(chunks))]
    )
    print(f"Indexed {len(chunks)} chunks from {os.path.basename(file_path)}\n")

# ─────────────────────────────────────────
# RAG QUERY FUNCTION
# same as before - retrieve then generate
# ─────────────────────────────────────────
def rag_query(question: str, n_results: int = 3) -> str:
    if collection.count() == 0:
        return "No documents indexed yet. Please add documents first."

    results = collection.query(
        query_texts=[question],
        n_results=min(n_results, collection.count())
    )

    retrieved_docs = results["documents"][0]
    sources = [m["source"] for m in results["metadatas"][0]]

    context = "\n\n".join([f"- {doc}" for doc in retrieved_docs])

    prompt = f"""You are a helpful assistant. Answer the question using ONLY the context provided below.
If the answer is not in the context, say "I don't have that information in the provided documents."

Context:
{context}

Question: {question}

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

    # show sources
    unique_sources = list(set(sources))
    answer += f"\n\nSources: {', '.join(unique_sources)}"
    return answer

# ─────────────────────────────────────────
# INTERACTIVE SYSTEM
# commands:
# 'add <filepath>' - index a new document
# 'quit' - exit
# anything else - ask a question
# ─────────────────────────────────────────
print("RAG System - Chat with Your Documents")
print("Commands:")
print("  add <filepath>  - load a PDF or TXT file")
print("  quit            - exit")
print("  anything else   - ask a question\n")

while True:
    user_input = input("You: ").strip()

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    elif user_input.lower().startswith("add "):
        file_path = user_input[4:].strip()
        if os.path.exists(file_path):
            index_document(file_path)
            print(f"Total chunks in database: {collection.count()}\n")
        else:
            print(f"File not found: {file_path}\n")

    else:
        if collection.count() == 0:
            print("No documents loaded yet. Use 'add <filepath>' to load a document.\n")
        else:
            answer = rag_query(user_input)
            print(f"AI: {answer}\n")