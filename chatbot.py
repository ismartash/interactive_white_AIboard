from langchain_groq.chat_models import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os


class TutorChatBot:
    def __init__(self):
        """Initialize the TutorChatBot with the necessary configurations."""
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        
        self.llm = ChatGroq(model_name="llama-3.3-70b-versatile", api_key=api_key)
        self.prompt_template = PromptTemplate(
            template="You are an experienced tutor. You have to answer based on user query. {user_input}",
            input_variables=["user_input"]
        )

    def respond(self, user_input):
        """Generate a response for the given user input."""
        chain = self.prompt_template | self.llm
        response = chain.invoke({"user_input": user_input})
        return response
