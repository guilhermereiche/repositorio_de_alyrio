from pathlib import Path
from datetime import date
import json

from model import PLATAFORMAS, model_movimento, nome_completo

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)
PRODUTOS_PATH = DATA_DIR / "produtos.json"
MOVIMENTOS_PATH = DATA_DIR / "movimentos.json"


# ---------- funções auxiliares (ler/escrever JSON) ----------
def _read_json(path):
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def _write_json(path, data):
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


# ---------- PRODUTOS (CRUD) ----------
def read_produtos():
    return _read_json(PRODUTOS_PATH)


def get_produto(produto_id):
    for p in read_produtos():
        if p["id"] == produto_id:
            return p
    return None


def find_variacao(nome, modelo, lado):
    """Procura um produto com a mesma peça + modelo + lado
    (ignora maiúsculas/minúsculas). Devolve o produto ou None."""
    for p in read_produtos():
        if (p["nome"].lower() == nome.lower()
                and p["modelo"].lower() == modelo.lower()
                and p["lado"] == lado):
            return p
    return None


def search_produtos(termo):
    """Busca pelo nome completo. Todas as palavras digitadas precisam aparecer.
    Ex: 'parabarro onix' acha Parabarro Onix - Direito e - Esquerdo.
    Termo vazio devolve todos."""
    palavras = termo.lower().split()
    resultado = []
    for p in read_produtos():
        texto = nome_completo(p).lower()
        if all(palavra in texto for palavra in palavras):
            resultado.append(p)
    return resultado


def create_produto(produto_dict):
    produtos = read_produtos()
    novo_id = max((p["id"] for p in produtos), default=0) + 1
    produto_dict["id"] = novo_id
    produtos.append(produto_dict)
    _write_json(PRODUTOS_PATH, produtos)
    return novo_id


def update_produto(produto_id, **campos):
    """Atualiza campos de um produto. Ex: update_produto(3, alerta=10)"""
    produtos = read_produtos()
    for p in produtos:
        if p["id"] == produto_id:
            p.update(campos)
            _write_json(PRODUTOS_PATH, produtos)
            return True
    return False


def delete_produto(produto_id):
    produtos = read_produtos()
    restantes = [p for p in produtos if p["id"] != produto_id]
    if len(restantes) == len(produtos):
        return False
    _write_json(PRODUTOS_PATH, restantes)

    # apaga também o histórico desse produto
    movimentos = [m for m in read_movimentos() if m["produto_id"] != produto_id]
    _write_json(MOVIMENTOS_PATH, movimentos)
    return True


# ---------- MOVIMENTAÇÕES (entradas e saídas) ----------
def read_movimentos():
    return _read_json(MOVIMENTOS_PATH)


def movimentos_do_produto(produto_id):
    return [m for m in read_movimentos() if m["produto_id"] == produto_id]


def _add_movimento(movimento):
    movimentos = read_movimentos()
    movimentos.append(movimento)
    _write_json(MOVIMENTOS_PATH, movimentos)


def registrar_saida(produto_id, quantidade, plataforma):
    """Dá baixa no estoque. Devolve (True/False, mensagem)."""
    produto = get_produto(produto_id)
    if produto is None:
        return False, "Produto não encontrado."
    if quantidade > produto["quantidade"]:
        return False, f"Estoque insuficiente (só tem {produto['quantidade']})."

    update_produto(produto_id, quantidade=produto["quantidade"] - quantidade)
    _add_movimento(model_movimento(produto_id, "saida", quantidade, plataforma))
    return True, "Saída registrada!"


def registrar_entrada(produto_id, quantidade):
    """Soma ao estoque (chegou remessa nova). Devolve (True/False, mensagem)."""
    produto = get_produto(produto_id)
    if produto is None:
        return False, "Produto não encontrado."

    update_produto(produto_id, quantidade=produto["quantidade"] + quantidade)
    _add_movimento(model_movimento(produto_id, "entrada", quantidade))
    return True, "Entrada registrada!"


# ---------- CÁLCULOS ----------
def media_diaria(produto_id):
    """Média de unidades vendidas por dia, por plataforma e no geral.
    O período vai do dia da primeira saída registrada até hoje."""
    medias = {plataforma: 0.0 for plataforma in PLATAFORMAS}
    medias["Geral"] = 0.0

    saidas = [m for m in movimentos_do_produto(produto_id) if m["tipo"] == "saida"]
    if not saidas:
        return medias

    primeira = min(date.fromisoformat(m["data"]) for m in saidas)
    dias = (date.today() - primeira).days + 1

    for m in saidas:
        medias[m["plataforma"]] += m["quantidade"]
        medias["Geral"] += m["quantidade"]

    for chave in medias:
        medias[chave] /= dias
    return medias