# AI Symposium — UTB Chatbot Demo

A demo chatbot built for the AI Symposium at Tomas Bata University (UTB) in Zlín.
The chatbot uses a local LLM via [Ollama](https://ollama.com) and exposes a simple web UI through [Gradio](https://gradio.app).

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
- [Ollama](https://ollama.com) running locally with `llama3.1:8b` pulled:
  ```bash
  ollama pull llama3.1:8b
  ```

## Installation

```bash
# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Running the app

```bash
python chatbot_utb.py
```

Gradio will print a local URL (e.g. `http://127.0.0.1:7860`) — open it in your browser.
Pass `share=True` (already set) to also get a temporary public link.

To run one of the extended versions:

```bash
python next_steps/chatbot_utb_sytem_prompt_history_summarization_rag_extensions_mood.py
```