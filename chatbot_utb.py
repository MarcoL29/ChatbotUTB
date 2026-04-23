from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import gradio as gr



#llm = ChatOllama(model="llama3.1", temperature=0)
llm = ChatOllama(model="llama3.1:8b", temperature=0,
    base_url="http://10.5.32.17:11434" )

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