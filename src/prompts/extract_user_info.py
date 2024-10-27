from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=['user_input'],
    template="""
        Extraia as seguintes informações da entrada do usuário: idade, sexo, altura em cm, peso em kg e nível de atividade.
        onde o nível de atividade pode ser:
        - sedentário: pouco ou nenhum exercício
        - levemente ativo: exercício leve 1-3 dias por semana
        - moderadamente ativo: exercício moderado 3-5 dias por semana
        - muito ativo: exercício pesado 6-7 dias por semana
        - extremamente ativo: exercício pesado diariamente e atividades físicas rotineiras
        Formato de saída em JSON:
        {
            "age": [idade em anos],
            "sex": "[sexo]",
            "height_cm": [altura em cm],
            "weight_kg": [peso em kg],
            "activity_level": "[nível de atividade]"
        }
        Se alguma informação estiver faltando, deixe o campo como null.
        Entrada do usuário: {user_input}
        """,
)
