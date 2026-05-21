import os
import time
import gradio as gr
import ollama
import chromadb
import langchain
import langchain_text_splitters
from chromadb.config import Settings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")
CHROMA_HOST = os.getenv("CHROMA_HOST", "http://chroma:8000")
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "executives_usa_policies")
POLICY_PDF = os.getenv("POLICY_PDF", "/data/executives_usa_policies.pdf")

ollama_client = ollama.Client(host=OLLAMA_HOST)

chroma_client = chromadb.HttpClient(
    host="chroma",
    port=8000,
    settings=Settings(allow_reset=True),
)

collection = chroma_client.get_or_create_collection(name=CHROMA_COLLECTION)
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)

def ingest_pdf_if_needed():
    if collection.count() > 0:
        return

    docs = PyPDFLoader(POLICY_PDF).load()
    chunks = splitter.split_documents(docs)

    ids = []
    documents = []
    metadatas = []

    for i, chunk in enumerate(chunks):
        ids.append(f"{int(time.time_ns())}_{i}")
        documents.append(chunk.page_content)
        metadatas.append({
            "source": "executives_usa_policies.pdf",
            "page": chunk.metadata.get("page", None),
        })

    if documents:
        collection.add(ids=ids, documents=documents, metadatas=metadatas)

def ask(question, model, top_k):
    ingest_pdf_if_needed()

    try:
        results = collection.query(
            query_texts=[question],
            n_results=int(top_k),
        )
        docs = results.get("documents", [[]])[0]
        context = "\n\n".join(docs) if docs else ""
    except Exception as e:
        context = f"Context retrieval error: {e}"

    prompt = f"""Use the policy context below to answer the question.

POLICY CONTEXT:
{context}

QUESTION:
{question}
"""

    try:
        res = ollama_client.chat(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        answer = res["message"]["content"]
    except Exception as e:
        answer = f"Ollama error: {e}"

    return answer, context

with gr.Blocks() as demo:
    gr.Markdown("# Ollama + ChromaDB + Policy PDF")

    with gr.Row():
        model = gr.Textbox(value="phi4-mini:latest", label="Ollama model")
        top_k = gr.Slider(1, 10, value=3, step=1, label="Relevant chunks")

    question = gr.Textbox(lines=3, label="Question")
    btn = gr.Button("Ask")

    answer = gr.Textbox(lines=10, label="Answer")
    context = gr.Textbox(lines=10, label="Retrieved policy context")

    btn.click(ask, inputs=[question, model, top_k], outputs=[answer, context])

demo.launch(server_name="0.0.0.0", server_port=7860)
