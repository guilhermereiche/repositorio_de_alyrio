from datetime import date

# Locais fixos do estoque
LOCAIS = [
    "Andar de baixo - Grades",
    "Andar de baixo - Lado esquerdo das grades",
    "Andar de baixo - Lado direito das grades",
    "Andar de cima - Sala dos parabarros",
    "Andar de cima - Sala de lente/pisca",
    "Andar de cima - Sala de capas",
    "Andar de cima - Corredor",
]

# Plataformas onde a loja vende
PLATAFORMAS = ["Shopee", "TikTok", "Mercado Livre"]

# Lados da peça
LADOS = ["Esquerdo", "Direito", "Único"]


def model_produto(nome, modelo, lado, local, quantidade=0, alerta=5):
    """Estrutura um produto como um dicionário (o id é criado no control).
    nome: a peça (ex: Parabarro)
    modelo: o carro (ex: Onix, G5)
    lado: Esquerdo ou Direito
    """
    return {
        "nome": nome,
        "modelo": modelo,
        "lado": lado,
        "local": local,
        "quantidade": quantidade,
        "alerta": alerta,
        "criado": date.today().isoformat(),
    }


def nome_completo(produto):
    """Monta o nome para mostrar na tela. Ex: Parabarro Onix - Direito"""
    return f"{produto['nome']} {produto['modelo']} - {produto['lado']}"


def model_movimento(produto_id, tipo, quantidade, plataforma=None):
    """Estrutura uma movimentação de estoque.
    tipo: "entrada" (chegou mercadoria) ou "saida" (vendeu)
    plataforma: só faz sentido nas saídas
    """
    return {
        "produto_id": produto_id,
        "tipo": tipo,
        "quantidade": quantidade,
        "plataforma": plataforma,
        "data": date.today().isoformat(),
    }