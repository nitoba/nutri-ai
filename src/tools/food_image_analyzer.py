import base64

from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langgraph import ToolNode
from PIL import Image

from env import env


class FoodImageAnaliseTool(ToolNode):
    name: str = 'food_image_analyzer'
    description: str = """
        Use essa ferramenta para analisar imagens de pratos de comida que o usuário enviar.
        Descreva os alimentos presentes na imagem e crie uma tabela nutricional da refeição.
    """

    def __init__(self):
        # Initialize language model
        self.llm = ChatGroq(
            api_key=env.API_KEY,
            model='llama-3.2-90b-vision-preview',
            temperature=0,
        )
        super().__init__(name=self.name, description=self.description)

    def _run(self, image_path: str) -> str:
        # Open and encode the image
        image = Image.open(image_path)
        image_bytes = image.tobytes()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')

        # Instructions for LLM
        instructions = """
        Você é um especialista em nutrição que precisa analisar imagens de pratos de comida.
        Analise a imagem enviada para verificar se contém um prato de comida.
        Caso contenha, descreva os alimentos presentes e crie uma tabela nutricional detalhada.
        """

        # Prepare the message with instructions and the image
        message = [
            HumanMessage(
                content=[
                    {'type': 'text', 'text': instructions},
                    {
                        'type': 'image_url',
                        'image_url': {
                            'url': f'data:image/jpeg;base64,{image_base64}'
                        },
                    },
                ]
            ),
        ]

        # Execute the LLM with message and return response
        response = self.llm.invoke(message)
        return response

    async def _arun(self, image_path: str) -> str:
        # Placeholder for async compatibility
        return self._run(image_path)
