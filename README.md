# DocGPT

A local RAG (Retrieval-Augmented Generation) pipeline that lets you ask questions about any PDF document. Built with ChromaDB, Ollama embeddings, and Gemini as the LLM.

---

## How It Works

```
PDF
 ↓
Extract text (pypdf)
 ↓
Split into chunks (LangChain)
 ↓
Embed chunks (Ollama → nomic-embed-text-v2-moe)
 ↓
Store in ChromaDB (local vector database)
 ↓
User asks a question
 ↓
Embed question → query ChromaDB → retrieve top 4 chunks
 ↓
Send chunks + question to Gemini → get answer
 ↓
Display in Streamlit UI
```

---

## Project Structure

```
DocGPT/
├── app.py                  # Streamlit UI
├── ingest.py               # Extract text from PDF
├── chunks.py               # Split text into chunks
├── chunks_embeddings.py    # Embed chunks and store in ChromaDB
├── chroma_db/              # Local vector database (auto-generated)
├── files/                  # Extracted text files (auto-generated)
├── jsons/                  # Chunk JSON files (auto-generated)
├── pdfs/                   # Place your PDF here
├── .env                    # API keys (not pushed to GitHub)
└── .gitignore
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/shaikhsanan04/docGPT.git
cd docGPT
```

### 2. Install dependencies

```bash
pip install streamlit chromadb ollama langchain-text-splitters pypdf google-genai python-dotenv
```

### 3. Install and set up Ollama

Download Ollama from [ollama.com](https://ollama.com) and pull the embedding model:

```bash
ollama pull nomic-embed-text-v2-moe
```

### 4. Set up your Gemini API key

Create a `.env` file in the root directory:

```
GEMINI_API_KEY=your_api_key_here
```

Get a free key at [aistudio.google.com](https://aistudio.google.com/apikey).

### 5. Add your PDF

Place your PDF inside the `pdfs/` folder.

---

## Usage

Run the following scripts in order (one time only, when you add a new PDF):

```bash
python ingest.py
python chunks.py
python chunks_embeddings.py
```

Then launch the app:

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` and start asking questions.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| pypdf | Extract text from PDF |
| LangChain | Text splitting |
| Ollama (`nomic-embed-text-v2-moe`) | Local embeddings |
| ChromaDB | Local vector database |
| Gemini 2.5 Flash | LLM for answer generation |
| Streamlit | Web UI |

---

## Notes

- The `chroma_db/`, `files/`, `jsons/`, and `pdfs/` folders are excluded from the repo via `.gitignore`
- The embedding step is incremental — re-running `chunks_embeddings.py` will skip already stored chunks
- This project currently uses a fixed PDF as its knowledge base. Dynamic PDF upload via UI is a planned improvement

---

## Author

**Sanan Shaikh** — [github.com/shaikhsanan04](https://github.com/shaikhsanan04)
