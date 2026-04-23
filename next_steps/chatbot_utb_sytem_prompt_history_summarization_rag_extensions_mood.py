from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage
import gradio as gr
from datetime import datetime
from data import knowledge_base, system_prompt


# --- simple_rag_data.py ---


llm = ChatOllama(model="llama3.1")


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
        self.mood = 0

        self.chat_prompt_template = ChatPromptTemplate.from_messages([
            ("system","{system_message}"),
            ("system","Use primary this context to answer the user questions: \n {context}"),
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

    def get_context_info(self, prompt):
        query_lower = prompt.lower()
        matched_contexts = []

        for item in knowledge_base:
            if any(keyword in query_lower for keyword in item["keywords"]):
                matched_contexts.append(item["context"])

        if "time" in query_lower or "date" in query_lower:
            matched_contexts.append(f"Current time: {str(datetime.now())}")


        if not matched_contexts:
            return "No relevant context found."

        return "\n".join(matched_contexts)

    def get_session_history(self):
        if not self.history:
            self.history = InMemoryChatMessageHistory()
        print("------------ HISTORY ------------")
        print(self.history)
        print("------------ HISTORY END ------------")
        return self.history

    def update_mood(self, msg):

        text = msg.lower()

        positive_words = [
            "thanks", "thank you", "great", "awesome", "good", "nice", "cool",
            "love", "fun", "amazing", "wow", "perfect", "yay", "sweet", "like"
        ]

        negative_words = [
            "bad", "hate", "boring", "stupid", "dumb", "annoying", "lame",
            "terrible", "awful", "ugh", "noob", "sucks", "mad", "angry", "sad"
        ]

        # Mood adjustment logic
        if any(word in text for word in positive_words):
            self.mood += 1
        elif any(word in text for word in negative_words):
            self.mood -= 1

        # Keep mood within range
        self.mood = max(-5, min(5, self.mood))

        return self.mood


    def chat(self, prompt):
        print(f"User prompt: {prompt}")

        print(self.update_mood(prompt))

        self.summarize_history(self.get_session_history())

        result = self.chat_with_memory.invoke({
            "system_message": f"{self.system_prompt}\n Your current mood in the range from -5 (really bad) to 5 (really good) is {self.mood}",
            "context": self.get_context_info(prompt),
            "question": prompt,
        })

        return result



if __name__ == "__main__":
    app = create_chatbot_interface(UTBChatBot(llm, system_prompt))
    app.launch(share=True)