import uuid

from fpdf import FPDF
from langchain_core.tools import tool


@tool
def generate_meal_plan_pdf(meal_plan: dict) -> str:
    """
    Gera um PDF contendo o plano alimentar fornecido.

    Args:
        meal_plan (dict): Dicionário contendo as informações do plano alimentar, onde cada chave representa uma refeição (ex.: "Café da manhã", "Almoço") e o valor é uma lista de itens dessa refeição.

    Returns:
        str: Caminho para o arquivo PDF gerado.
    """
    # Cria uma instância do PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    pdf.cell(200, 10, txt='Plano Alimentar', ln=True, align='C')

    # Adiciona o plano alimentar ao PDF
    for meal, items in meal_plan.items():
        pdf.ln(10)  # Espaço entre as seções de refeições
        pdf.set_font('Arial', style='B', size=12)
        pdf.cell(0, 10, txt=meal, ln=True)  # Nome da refeição

        # Lista os itens de cada refeição
        pdf.set_font('Arial', size=10)
        for item in items:
            pdf.cell(0, 10, txt=f'- {item}', ln=True)

    # Salva o PDF em um arquivo
    file_path = f'/mnt/data/{uuid.uuid4()}_meal_plan.pdf'
    pdf.output(file_path)

    return {'pdf_path': file_path, 'file_name': file_path.split('/')[-1]}
