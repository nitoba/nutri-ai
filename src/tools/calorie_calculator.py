from langchain_core.tools import tool


@tool
def calculate_calories(
    age: int, sex: str, height_cm: float, weight_kg: float, activity_level: str
) -> str:
    """
    Calcula o BMR (Taxa Metabólica Basal) e o TDEE (Gasto Energético Diário Total) usando a fórmula de Harris-Benedict.

    Args:
        age (int): Idade em anos
        sex (str): Sexo ("masculino" ou "feminino")
        height_cm (float): Altura em centímetros
        weight_kg (float): Peso em quilogramas
        activity_level (str): Nível de atividade ("sedentário", "pouco ativo", "moderadamente ativo", "muito ativo" ou "extremamente ativo")

    Returns:
        str: Uma string formatada contendo os valores calculados de BMR e TDEE
    """
    # Calculate BMR using Harris-Benedict formula
    if sex.lower() in ['masculino', 'homem']:
        bmr = 66 + (13.7 * weight_kg) + (5 * height_cm) - (6.8 * age)
    elif sex.lower() in ['feminino', 'mulher']:
        bmr = 655 + (9.6 * weight_kg) + (1.8 * height_cm) - (4.7 * age)
    else:
        return 'Sexo deve ser "masculino" ou "feminino".'

    # Map activity level to activity factor
    activity_levels = {
        'sedentário': 1.2,
        'pouco ativo': 1.375,
        'moderadamente ativo': 1.55,
        'muito ativo': 1.725,
        'extremamente ativo': 1.9,
    }

    activity_factor = activity_levels.get(activity_level.lower())
    if activity_factor is None:
        return 'Nível de atividade inválido.'

    # Calculate TDEE
    tdee = bmr * activity_factor

    result = (
        f'Seu BMR (Taxa Metabólica Basal) é {bmr:.2f} calorias por dia.\n'
        f'Seu TDEE (Gasto Energético Diário Total) é {tdee:.2f} calorias por dia.'
    )

    return result
