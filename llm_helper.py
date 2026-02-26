from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

llm = ChatGroq(groq_api_key = os.getenv("GROQ_API_KEY"),model_name = "openai/gpt-oss-120b",temperature=0.2)

# CHECKING LOGICS
if __name__ == "__main__":
    answer = llm.invoke("If Pratham is seated on the left to Shivam who is seated to the left of Harsham, then who is seated in the middle, Harsham,Shivam or Pratham?")
    print(answer.content)