from pathlib import Path
from datetime import date, datetime, timedelta
import json
import os
import shutil
import sys
import traceback

from model import PLATAFORMAS, model_movimento, nome_completo

# ---------- configurações ----------
JANELA_DIAS = 30        # a média de saída considera no máximo os últimos 30 dias
DIAS_DE_BACKUP = 30     # quantos dias de backup guardar


def _pasta_base():
    """Pasta onde ficam os dados. Funciona tanto rodando o .py
    quanto depois de virar um .exe."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


DATA_DIR = _pasta_base() / "data"
DATA_DIR.mkdir(exist_ok=True)
BACKUP_DIR = DATA_DIR / "backups"
PRODUTOS_PATH = DATA_DIR / "produtos.json"
MOVIMENTOS_PATH = DATA_DIR / "movimentos.json"
ERROS_LOG = DATA_DIR / "erros.log"


# ---------- funções auxiliares (ler/escrever JSON com segurança) ----------
def _json_valido(path):
    """True se o arquivo existe e é um JSON legível."""
    if not path.exists():
        return False
    try:
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except (json.JSONDecodeError, OSError):
        return False


def _ultimo_backup(path):
    """Procura o backup válido mais recente de um arquivo."""
    if not BACKUP_DIR.exists():
        return None
    pastas = sorted((p for p in BACKUP_DIR.iterdir() if p.is_dir()), reverse=True)
    for pasta in pastas:
        candidato = pasta / path.name
        if _json_valido(candidato):
            return candidato
    return None


def _tratar_arquivo_corrompido(path):
    """Guarda uma cópia do arquivo quebrado e tenta restaurar do backup."""
    carimbo = datetime.now().strftime("%Y%m%d-%H%M%S")
    copia = path.with_name(f"{path.stem}.corrompido-{carimbo}{path.suffix}")
    shutil.copy2(path, copia)
    print(f"\nATENÇÃO: o arquivo {path.name} estava corrompido.")
    print(f"Uma cópia dele foi guardada como {copia.name}.")

    backup = _ultimo_backup(path)
    if backup is None:
        print("Nenhum backup encontrado. Começando com a lista vazia.")
        return []

    print(f"Dados restaurados do backup de {backup.parent.name}.")
    dados = json.loads(backup.read_text(encoding="utf-8"))
    _write_json(path, dados)
    return dados


def _read_json(path):
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return _tratar_arquivo_corrompido(path)


def _write_json(path, data):
    """Grava num arquivo temporário e só depois troca pelo definitivo.
    Assim, se o programa travar no meio, o arquivo original não quebra."""
    temporario = path.with_suffix(".tmp")
    temporario.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    os.replace(temporario, path)


# ---------- BACKUP E LOG ----------
def fazer_backup():
    """Copia os dados para data/backups/AAAA-MM-DD (uma vez por dia)
    e apaga backups mais antigos que DIAS_DE_BACKUP."""
    pasta = BACKUP_DIR / date.today().isoformat()
    if pasta.exists():
        return

    arquivos = [a for a in (PRODUTOS_PATH, MOVIMENTOS_PATH) if _json_valido(a)]
    if not arquivos:
        return

    pasta.mkdir(parents=True)
    for arquivo in arquivos:
        shutil.copy2(arquivo, pasta / arquivo.name)

    pastas = sorted(p for p in BACKUP_DIR.iterdir() if p.is_dir())
    for antiga in pastas[:-DIAS_DE_BACKUP]:
        shutil.rmtree(antiga, ignore_errors=True)


def registrar_erro():
    """Salva o erro inesperado em data/erros.log (chamar dentro de um except)."""
    with open(ERROS_LOG, "a", encoding="utf-8") as arquivo:
        arquivo.write(f"--- {datetime.now():%Y-%m-%d %H:%M:%S} ---\n")
        arquivo.write(traceback.format_exc() + "\n")


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

    _add_movimento(model_movimento(produto_id, "saida", quantidade, plataforma))
    update_produto(produto_id, quantidade=produto["quantidade"] - quantidade)
    return True, "Saída registrada!"


def registrar_entrada(produto_id, quantidade):
    """Soma ao estoque (chegou remessa nova). Devolve (True/False, mensagem)."""
    produto = get_produto(produto_id)
    if produto is None:
        return False, "Produto não encontrado."

    _add_movimento(model_movimento(produto_id, "entrada", quantidade))
    update_produto(produto_id, quantidade=produto["quantidade"] + quantidade)
    return True, "Entrada registrada!"


def desfazer_ultimo_movimento(produto_id):
    """Apaga o último lançamento do produto e devolve o estoque ao que era.
    Útil quando alguém digitou a quantidade ou a plataforma errada."""
    produto = get_produto(produto_id)
    if produto is None:
        return False, "Produto não encontrado."

    movimentos = read_movimentos()
    posicoes = [i for i, m in enumerate(movimentos) if m["produto_id"] == produto_id]
    if not posicoes:
        return False, "Esse produto ainda não tem lançamentos."

    ultimo = movimentos[posicoes[-1]]
    if ultimo["tipo"] == "saida":
        nova_quantidade = produto["quantidade"] + ultimo["quantidade"]
    else:
        nova_quantidade = produto["quantidade"] - ultimo["quantidade"]
        if nova_quantidade < 0:
            return False, "Não dá pra desfazer: o estoque ficaria negativo."

    movimentos.pop(posicoes[-1])
    _write_json(MOVIMENTOS_PATH, movimentos)
    update_produto(produto_id, quantidade=nova_quantidade)
    return True, "Último lançamento desfeito."


# ---------- CÁLCULOS ----------
def media_diaria(produto_id):
    """Média de unidades vendidas por dia, por plataforma e no geral.

    Período considerado: da primeira venda do produto até hoje,
    mas olhando no máximo os últimos JANELA_DIAS dias.
    Dias sem venda contam como dias com zero venda.

    Devolve (medias, dias): medias é um dicionário e dias é o tamanho do
    período usado (0 se o produto nunca vendeu)."""
    hoje = date.today()

    saidas = [m for m in movimentos_do_produto(produto_id) if m["tipo"] == "saida"]
    medias = {plataforma: 0.0 for plataforma in PLATAFORMAS}
    if not saidas:
        medias["Geral"] = 0.0
        return medias, 0

    primeira_venda = min(date.fromisoformat(m["data"]) for m in saidas)
    inicio_janela = hoje - timedelta(days=JANELA_DIAS - 1)
    inicio = max(primeira_venda, inicio_janela)
    dias = max(1, (hoje - inicio).days + 1)

    total = 0
    for m in saidas:
        if date.fromisoformat(m["data"]) < inicio:
            continue  # venda antiga, fora da janela
        # .get evita erro se o nome da plataforma mudou ou não existe mais na lista
        plataforma = m.get("plataforma") or "Outra"
        medias[plataforma] = medias.get(plataforma, 0.0) + m["quantidade"]
        total += m["quantidade"]

    for plataforma in medias:
        medias[plataforma] /= dias
    medias["Geral"] = total / dias
    return medias, dias