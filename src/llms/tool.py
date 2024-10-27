from langchain_groq import ChatGroq

from env import env

llm = ChatGroq(
    model='llama-3.1-70b-versatile', api_key=env.API_KEY, temperature=0
)
