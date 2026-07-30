# Day 19 - FastAPI: Deploy your AI as an API

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cohere
import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader
import io
import os
API_KEY = ""
cohere_client = cohere.ClientV2(api_key=API_KEY)
cohere_ef = embedding_functions.CohereEmbeddingFunction(
    api_key=API_KEY,
    model_name="embed-v4.0"
)
chroma_client = chromadb.PersistentClient(path="./fastapi_db")
existing = [c.name for c in chroma_client.list_collections()]
if "documents" in existing:
    collection = chroma_client.get_collection("documents", embedding_function=cohere_ef)
else:
    collection = chroma_client.create_collection("documents", embedding_function=cohere_ef)

# FASTAPI APP - title and description appear in auto-generated docs
# CORS middleware allows frontend apps to call your API
app = FastAPI(
    title="AI RAG API",
    description="Upload documents and chat with them using AI",
    version="1.0"
)
# CORS - allows any frontend to call this API
# in production restrict this to your actual domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# REQUEST AND RESPONSE MODELS
# Pydantic models define the shape of data
# FastAPI validates incoming data automatically
# if data doesn't match the model, FastAPI returns 422 error
class ChatRequest(BaseModel):
    question: str           # required field
    n_results: int = 3      # optional field with default
class ChatResponse(BaseModel):
    answer: str
    sources: list[str]
    chunks_used: int
class StatusResponse(BaseModel):
    status: str
    total_chunks: int
    message: str

# HELPER FUNCTIONS - same logic as Day 17
def chunk_text(text: str) -> list:
    chunks, start = [], 0
    while start < len(text):
        chunk = text[start:start + 500].strip()
        if chunk:
            chunks.append(chunk)
        start += 450
    return chunks
def rag_query(question: str, n_results: int = 3) -> dict:
    results = collection.query(
        query_texts=[question],
        n_results=min(n_results, collection.count())
    )

    chunks = results["documents"][0]
    sources = list(set(m["source"] for m in results["metadatas"][0]))
    context = "\n\n".join(chunks)

    prompt = f"""Answer using ONLY the context below.
If not found say "I don't have that information in the documents."

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

    return {
        "answer": answer,
        "sources": sources,
        "chunks_used": len(chunks)
    }


# ENDPOINTS
# @app.get = handles GET requests
# @app.post = handles POST requests
# the path is the URL: /health, /upload, /chat
# GET /health - check if API is running
# every production API needs this
# deployment platforms ping this to verify the app started
@app.get("/health", response_model=StatusResponse)
def health_check():
    return StatusResponse(
        status="healthy",
        total_chunks=collection.count(),
        message="API is running"
    )

# POST /upload - upload a PDF and index it
# UploadFile handles file uploads automatically
@app.post("/upload", response_model=StatusResponse)
async def upload_document(file: UploadFile = File(...)):
    # validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files supported")

    # read file contents
    contents = await file.read()

    # extract text from PDF
    reader = PdfReader(io.BytesIO(contents))
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    if not text.strip():
        raise HTTPException(status_code=400, detail="No text found in PDF")

    # chunk and index
    chunks = chunk_text(text)
    offset = collection.count()
    collection.add(
        documents=chunks,
        metadatas=[{"source": file.filename} for _ in chunks],
        ids=[f"chunk_{offset + i}" for i in range(len(chunks))]
    )

    return StatusResponse(
        status="success",
        total_chunks=collection.count(),
        message=f"Indexed {len(chunks)} chunks from {file.filename}"
    )

# POST /chat - ask a question about your documents
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    if collection.count() == 0:
        raise HTTPException(
            status_code=400,
            detail="No documents uploaded yet. Use /upload first."
        )

    result = rag_query(request.question, request.n_results)
    return ChatResponse(**result)

# GET /documents - list all indexed documents
@app.get("/documents")
def list_documents():
    if collection.count() == 0:
        return {"documents": [], "total_chunks": 0}

    results = collection.get()
    sources = list(set(m["source"] for m in results["metadatas"]))
    return {
        "documents": sources,
        "total_chunks": collection.count()
    }