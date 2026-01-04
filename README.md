# RAG_CHATBOT ✅

A Retrieval-Augmented Generation (RAG) chatbot for medical documents. The app ingests PDF documents, builds a vector index in Pinecone using embeddings from a HuggingFace embedding model, and answers user questions by retrieving relevant passages and invoking an LLM (via OpenAI) with a context-only prompt.

---

##  Quickstart — Setup & Run (Windows-focused)

### 1) Prerequisites
- Python 3.11+
- A Pinecone account & API key
- An OpenAI key

Create a `.env` file in the project root with:

```ini
PINECONE_API_KEY="your-pinecone-api-key"
OPENAI_API_KEY="your-openai-api-key"
```

### 2) Create and activate a virtual environment (Windows PowerShell)

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Build the vector index (ingest PDFs from `Data/`)

```bash
python store_index.py
```

This loads PDFs from `Data/`, splits them into chunks (500 token-ish, 50 overlap), computes embeddings (`sentence-transformers/all-MiniLM-L6-v2`) and writes the vectors to a Pinecone index named `medical-bot`.

### 5) Run the Flask app

```bash
python app.py
```

Open http://localhost:8080/ and ask questions via the UI (`templates/chatbot.html`).



---

##  High-level Architecture

1. Data ingestion
   - `src/helper.py` uses `DirectoryLoader` / `PyPDFLoader` to load PDFs from `Data/`.
2. Preprocessing
   - Documents are filtered for minimal metadata and split using `RecursiveCharacterTextSplitter` (chunk_size=500, overlap=50).
3. Embeddings
   - Embeddings are produced using `HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")`, producing 384-d vectors.
4. Storage
   - Vectors are stored in Pinecone (`medical-bot` index). `store_index.py` creates the index if missing.
5. Retrieval & Response
   - The Flask app (`app.py`) creates a retriever (k=3) from the Pinecone index and a retrieval chain that calls the LLM (`ChatOpenAI`) with the prompt template from `src/prompt.py`.
6. UI
   - `templates/chatbot.html` provides a minimal chat interface.

Flow: PDFs -> Loader -> Split -> Embeddings -> Pinecone index -> Retrieval -> LLM -> User answer

---

## RAG Design Decisions & Trade-offs

- Embedding Model: `sentence-transformers/all-MiniLM-L6-v2` (HuggingFace)
  - Pros: free to use, fast, good general-purpose semantic retrieval, privacy-friendly (runs locally).
  - Cons: lower representational power vs larger/specialized embedding models (e.g., OpenAI text-embedding-3), may reduce retrieval precision.

- Vector DB: Pinecone (Serverless)
  - Pros: managed, fast, simple index creation and scaling, supports namespaces and metadata filtering.
  - Cons: cost as data grows; vendor lock-in vs open-source options (Milvus, Weaviate)

- Retrieval params: `k=3` and `chunk_size=500` with 50 overlap
  - Pros: smaller context passed to LLM => lower latency/cost; overlap reduces split-induced context loss.
  - Trade-off: too small k or chunk size could miss necessary context; too large increases cost and hallucination risk.

- Prompt & Safety
  - The system prompt forces the assistant to **only use the provided context** and to answer “I don’t know based on the provided medical documents.” when appropriate—this reduces hallucinations but may increase "I don’t know" cases.

- LLM: `ChatOpenAI(model_name="gpt-5", temperature=0.2)`
  - Lower temperature favors consistent answers. Production choices can use smaller, cheaper LLMs for latency/cost trade-offs or larger models for higher quality.

---

##  Scaling to Enterprise Usage


- Indexing & Sharding
  
  - Use vector DB features for metadata filters ( source, page content).

- Latency & Cost Optimization
  - Batch embedding requests, cache embeddings for unchanged documents, use a faster/smaller embedding model in warm paths.


- Privacy
  - Use private/self-hosted embedding models or hosted options with strict data use terms.
  - Consider on-prem deployments for sensitive data.

- Cost Controls
  - Rate limiting, budget alerts for API usage
---

## Development & Testing

- Ingest test PDFs into `Data/` and run `python store_index.py` to populate Pinecone for local testing.
- The `tests/trials.ipynb` notebook can be used to experiment with retrieval and prompts.

---

## Troubleshooting

- Missing env vars: ensure `.env` variables are loaded and exported.
- Pinecone index errors: verify `PINECONE_API_KEY` and region configuration.
- Docker build fails: fix Dockerfile `FROM PTHON` -> `FROM python`.

---














