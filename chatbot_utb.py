from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import gradio as gr
import os

load_dotenv()

# --- Option A: Ollama (local) ---
llm = ChatOllama(model="llama3.1:8b", temperature=0)
#llm = ChatOllama(model="llama3.1:8b", temperature=0,
#    base_url="http://10.5.32.17:11434")

# --- Option B: Groq (cloud) ---
# Requires: pip install langchain-groq
# Get your API key at https://console.groq.com and put it in .env as GROQ_API_KEY
# from langchain_groq import ChatGroq
# llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0, api_key=os.getenv("GROQ_API_KEY"))

def create_chatbot_interface(chatbot):
    def generate_response(user_input):
        return chatbot.chat(user_input)

    with gr.Blocks() as app:
        with gr.Row():
            text_input = gr.Textbox(label="Your Message", placeholder="Enter your message and pres ENTER")

        output_area = gr.Textbox(label="Chatbot response", interactive=False, lines=10)

        text_input.submit(generate_response, inputs=text_input, outputs=output_area)

    return app




class UTBChatBot:
    def __init__(self, llm):
        self.llm:ChatOllama = llm


    def chat(self, prompt):
        print(f"User prompt: {prompt}")

        result = self.llm.invoke(prompt)

        return result.content



if __name__ == "__main__":
    app = create_chatbot_interface(UTBChatBot(llm))
    app.launch(share=True)