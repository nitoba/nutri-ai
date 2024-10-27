import json

from langchain_core.output_parsers.json import JsonOutputParser
from langchain_core.tools import tool

from llms.tool import llm
from prompts.extract_user_info import prompt


@tool
def extract_user_info(user_input: str) -> dict:
    """
    Extrai informações pessoais do usuário a partir de uma entrada em linguagem natural.

    Args:
        user_input (str): Texto em linguagem natural contendo informações do usuário

    Returns:
        dict: Dicionário com as informações extraídas do usuário contendo idade, sexo, altura, peso e nível de atividade
    """

    chain = prompt | llm | JsonOutputParser()

    try:
        extracted_info = chain.invoke({'user_input': user_input})
        return extracted_info
    except json.JSONDecodeError:
        return {}
