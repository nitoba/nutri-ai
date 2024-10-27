from langchain_groq import ChatGroq

from env import env

llm = ChatGroq(
    api_key=env.API_KEY,
    model='llama-3.2-90b-text-preview',
    temperature=0.1,
)
