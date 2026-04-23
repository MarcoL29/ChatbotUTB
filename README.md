# AI Symposium — UTB Chatbot Demo

A demo chatbot built for the AI Symposium at Tomas Bata University (UTB) in Zlín.
The chatbot exposes a simple web UI through [Gradio](https://gradio.app) and supports two LLM backends — a local one via [Ollama](https://ollama.com) or a cloud one via [Groq](https://groq.com).

The `next_steps/` directory contains progressive versions of the chatbot, each adding a new feature:

| File | Added feature |
|------|--------------|
| `chatbot_utb.py` | Baseline — plain LLM call |
| `next_steps/chatbot_utb_sytem_prompt.py` | System prompt |
| `next_steps/chatbot_utb_sytem_prompt_history.py` | Conversation history |
| `next_steps/chatbot_utb_sytem_prompt_history_summarization.py` | History summarization |
| `next_steps/chatbot_utb_sytem_prompt_history_summarization_rag.py` | RAG (knowledge base) |
| `next_steps/chatbot_utb_sytem_prompt_history_summarization_rag_extensions.py` | Extensions |
| `next_steps/chatbot_utb_sytem_prompt_history_summarization_rag_extensions_mood.py` | Mood tracking |

## Prerequisites

- Python 3.10+
- One of the two LLM backends below (your choice)

### Option A — Ollama (local, no API key needed)

Install Ollama from [ollama.com](https://ollama.com), then pull the model:

```bash
ollama pull llama3.1:8b
```

### Option B — Groq (cloud, free tier available)

1. Create a free account at [console.groq.com](https://console.groq.com) and generate an API key.
2. Copy the env template and fill in your key:
   ```bash
   cp .env.template .env
   # then edit .env and set GROQ_API_KEY=gsk_...
   ```

## Installation

```bash
# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Choosing the LLM backend

Open `chatbot_utb.py` and toggle the two blocks near the top of the file:

```python
# --- Option A: Ollama (local) ---
# llm = ChatOllama(model="llama3.1:8b", temperature=0, base_url="http://...")

# --- Option B: Groq (cloud) ---
from langchain_groq import ChatGroq
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0, api_key=os.getenv("GROQ_API_KEY"))
```

Comment out whichever option you don't want and uncomment the other one.

## Running the app

```bash
python chatbot_utb.py
```

Gradio will print a local URL (e.g. `http://127.0.0.1:7860`) — open it in your browser.
`share=True` is already set, so you also get a temporary public link printed to the console.

To run one of the extended versions:

```bash
python next_steps/chatbot_utb_sytem_prompt_history_summarization_rag_extensions_mood.py
```