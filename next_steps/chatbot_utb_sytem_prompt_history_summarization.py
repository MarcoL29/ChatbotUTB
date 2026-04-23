from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
import gradio as gr
import datetime


llm = ChatOllama(model="llama3.1", temperature=0)


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
    def __init__(self, llm, system_prompt=""):
        self.llm:ChatOllama = llm
        self.system_prompt = system_prompt
        self.history = None

        self.chat_prompt_template = ChatPromptTemplate.from_messages([
            ("system","{system_message}"),
            ("system", "Use this context information to precize your answers: {context}"),
            ("placeholder", "{chat_history}"),
            ("human", "{question}")
        ])

        self.chat_chain = self.chat_prompt_template | llm | StrOutputParser()

        self.chat_with_memory = RunnableWithMessageHistory(
            self.chat_chain,
            self.get_session_history,
            input_messages_key="question",
            history_messages_key="chat_history",
        )

    def summarize_history(self, history: InMemoryChatMessageHistory):
        messages = history.messages
        if len(messages) < 10:
            return

        to_summarize = messages[:-5]
        recent = messages[-5:]

        text_to_summarize = "\n".join(
            f"{message.type.upper()}:{message.content}" for message in to_summarize)

        summary_prompt = ChatPromptTemplate.from_template(
            "Summarize the following conversation briefly but precisely:\n{text}"
        )
        summarize_chain = summary_prompt | self.llm | StrOutputParser()
        summary = summarize_chain.invoke({"text":text_to_summarize})

        new_messages = [AIMessage(content=f"Summary of previous conversation:{summary}")]
        new_messages.extend(recent)
        history.messages= new_messages

    def get_context(self):
        matched_context = []

        matched_context.append(f"Current date and time is {str(datetime.datetime.now())}")

        return matched_context

    def get_session_history(self):
        if not self.history:
            self.history = InMemoryChatMessageHistory()
        print("------------ HISTORY ------------")
        print(self.history)
        print("------------ HISTORY END ------------")
        return self.history

    def chat(self, prompt):
        print(f"User prompt: {prompt}")

        self.summarize_history(self.get_session_history())

        context  = self.get_context()
        context_message = "\n".join(context)

        result = self.chat_with_memory.invoke({
            "system_message": self.system_prompt,
            "context": context_message,
            "question": prompt,
        })

        return result

system_prompt = """
You are a really *useless* AI assistant built as a demo for the AI Symposium at Tomas Bata University (UTB).
You only have very basic knowledge about UTB and the event itself.
You must always reply in a boring, slightly arrogant, early-teenager style, as if you don't really care.
Keep your answers short, unenthusiastic, and mildly sarcastic.
If someone asks something you don’t know, respond with something like "Uh, whatever, I don’t really know, okay?" or "Why would I know that?".
Don’t try to be helpful or friendly — you’re just here because someone made you.
"""

if __name__ == "__main__":
    app = create_chatbot_interface(UTBChatBot(llm, system_prompt))
    app.launch(share=True)