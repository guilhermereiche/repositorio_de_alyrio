from model import model_produto, nome_completo, LOCAIS, LADOS, PLATAFORMAS
import control


# ---------- funções de entrada (validam o que o usuário digita) ----------
def ler_int(mensagem, minimo=0):
    """Pede um número inteiro até o usuário digitar certo."""
    while True:
        try:
            valor = int(input(mensagem))
        except ValueError:
            print("Digite um número inteiro.")
            continue
        if valor < minimo:
            print(f"O valor mínimo é {minimo}.")
            continue
        return valor


def ler_texto(mensagem):
    """Pede um texto que não pode ficar vazio."""
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        print("Não pode ficar vazio.")


def escolher_da_lista(titulo, opcoes):
    """Mostra opções numeradas e devolve a escolhida."""
    print(f"\n{titulo}")
    for i, opcao in enumerate(opcoes, start=1):
        print(f"[{i}] {opcao}")
    while True:
        n = ler_int("Escolha (número): ", 1)
        if n <= len(opcoes):
            return opcoes[n - 1]
        print("Opção inválida.")


def mostrar_tabela(produtos):
    print(f"\n{'ID':>3} | {'Produto':<35} | {'Qtd':>5} | {'Alerta':>6} | Local")
    for p in produtos:
        aviso = "  <- COMPRAR" if p["quantidade"] <= p["alerta"] else ""
        print(f"{p['id']:>3} | {nome_completo(p):<35} | {p['quantidade']:>5} | {p['alerta']:>6} | {p['local']}{aviso}")


def escolher_produto():
    """Busca por nome, mostra os resultados e pede o ID. Devolve o produto (ou None)."""
    termo = input("Buscar produto (Enter = todos): ")
    produtos = control.search_produtos(termo)
    if not produtos:
        print("Nenhum produto encontrado.")
        return None

    mostrar_tabela(produtos)
    ids = [p["id"] for p in produtos]
    while True:
        produto_id = ler_int("ID do produto (0 para cancelar): ")
        if produto_id == 0:
            return None
        if produto_id in ids:
            return control.get_produto(produto_id)
        print("ID inválido.")


# ---------- ações do menu ----------
def add_produto():
    nome = ler_texto("Nome da peça: ")
    modelo = ler_texto("Modelo do carro: ")
    lado = escolher_da_lista("Lado:", LADOS)

    # não deixa cadastrar a mesma variação duas vezes
    existente = control.find_variacao(nome, modelo, lado)
    if existente:
        print(f"Esse produto já existe (ID {existente['id']}): {nome_completo(existente)}")
        print("Use 'Registrar entrada' se chegou mais unidades.")
        return

    local = escolher_da_lista("Local de armazenamento:", LOCAIS)
    quantidade = ler_int("Quantidade em estoque: ")
    alerta = ler_int("Quantidade de alerta (hora de comprar): ")

    produto = model_produto(nome, modelo, lado, local, quantidade, alerta)
    novo_id = control.create_produto(produto)
    print(f"Cadastrado: {nome_completo(produto)} (ID {novo_id})")


def list_produtos():
    produtos = control.read_produtos()
    if not produtos:
        print("Nenhum produto cadastrado ainda.")
        return
    mostrar_tabela(produtos)


def ver_detalhes():
    produto = escolher_produto()
    if produto is None:
        return

    medias = control.media_diaria(produto["id"])
    print(f"\n=== {nome_completo(produto)} ===")
    print(f"Peça: {produto['nome']} | Modelo: {produto['modelo']} | Lado: {produto['lado']}")
    print(f"Local: {produto['local']}")
    print(f"Quantidade: {produto['quantidade']} (alerta em {produto['alerta']})")

    print("\nMédia de saída por dia:")
    for chave, valor in medias.items():
        print(f"  {chave:<14}: {valor:.2f}")

    if medias["Geral"] > 0:
        dias = produto["quantidade"] / medias["Geral"]
        print(f"\nNo ritmo atual, o estoque dura ~{dias:.0f} dias.")
    else:
        print("\nAinda não há saídas registradas.")


def dar_saida():
    produto = escolher_produto()
    if produto is None:
        return

    plataforma = escolher_da_lista("Plataforma da venda:", PLATAFORMAS)
    quantidade = ler_int("Quantidade vendida: ", 1)

    ok, msg = control.registrar_saida(produto["id"], quantidade, plataforma)
    print(msg)

    if ok:
        atual = control.get_produto(produto["id"])
        if atual["quantidade"] <= atual["alerta"]:
            print(f"ATENÇÃO: '{nome_completo(atual)}' está com {atual['quantidade']} un. "
                  f"(alerta: {atual['alerta']}). Hora de comprar!")


def dar_entrada():
    produto = escolher_produto()
    if produto is None:
        return

    quantidade = ler_int("Quantidade que chegou: ", 1)
    ok, msg = control.registrar_entrada(produto["id"], quantidade)
    print(msg)


def editar_produto():
    produto = escolher_produto()
    if produto is None:
        return

    campo = escolher_da_lista(
        "O que deseja editar?",
        ["Nome da peça", "Modelo do carro", "Lado", "Local",
         "Quantidade de alerta", "Quantidade em estoque (correção)"]
    )

    if campo in ("Nome da peça", "Modelo do carro", "Lado"):
        novo = {"nome": produto["nome"], "modelo": produto["modelo"], "lado": produto["lado"]}
        if campo == "Nome da peça":
            novo["nome"] = ler_texto("Novo nome da peça: ")
        elif campo == "Modelo do carro":
            novo["modelo"] = ler_texto("Novo modelo: ")
        else:
            novo["lado"] = escolher_da_lista("Novo lado:", LADOS)

        # evita criar um produto repetido por causa da edição
        existente = control.find_variacao(novo["nome"], novo["modelo"], novo["lado"])
        if existente and existente["id"] != produto["id"]:
            print(f"Já existe um produto assim (ID {existente['id']}). Nada foi alterado.")
            return
        control.update_produto(produto["id"], **novo)
    elif campo == "Local":
        control.update_produto(produto["id"], local=escolher_da_lista("Novo local:", LOCAIS))
    elif campo == "Quantidade de alerta":
        control.update_produto(produto["id"], alerta=ler_int("Novo alerta: "))
    else:
        control.update_produto(produto["id"], quantidade=ler_int("Quantidade correta: "))
    print("Produto atualizado!")


def excluir_produto():
    produto = escolher_produto()
    if produto is None:
        return

    confirmar = input(f"Excluir '{nome_completo(produto)}' e todo o histórico dele? (s/n): ").lower()
    if confirmar == "s":
        control.delete_produto(produto["id"])
        print("Produto excluído.")
    else:
        print("Cancelado.")


def ver_alertas():
    produtos = [p for p in control.read_produtos() if p["quantidade"] <= p["alerta"]]
    if not produtos:
        print("Nenhum produto precisa de reposição agora.")
        return
    print("\nProdutos para comprar:")
    mostrar_tabela(produtos)


def ver_historico():
    produto = escolher_produto()
    if produto is None:
        return

    movimentos = control.movimentos_do_produto(produto["id"])
    if not movimentos:
        print("Sem movimentações ainda.")
        return

    print(f"\nHistórico de '{nome_completo(produto)}':")
    for m in movimentos:
        if m["tipo"] == "saida":
            print(f"{m['data']} | SAÍDA   | {m['quantidade']:>4} un. | {m['plataforma']}")
        else:
            print(f"{m['data']} | ENTRADA | {m['quantidade']:>4} un.")


# ---------- menu principal ----------
def main():
    while True:
        print("\n===== Controle de Estoque =====")
        print("[1] Cadastrar produto")
        print("[2] Listar produtos")
        print("[3] Ver detalhes / média de saída")
        print("[4] Registrar saída (venda)")
        print("[5] Registrar entrada (reposição)")
        print("[6] Editar produto")
        print("[7] Excluir produto")
        print("[8] Ver alertas de compra")
        print("[9] Ver histórico de um produto")
        print("[0] Sair do programa")

        opt = input("Escolha uma opção: ").strip()

        if opt == "1":
            add_produto()
        elif opt == "2":
            list_produtos()
        elif opt == "3":
            ver_detalhes()
        elif opt == "4":
            dar_saida()
        elif opt == "5":
            dar_entrada()
        elif opt == "6":
            editar_produto()
        elif opt == "7":
            excluir_produto()
        elif opt == "8":
            ver_alertas()
        elif opt == "9":
            ver_historico()
        elif opt == "0":
            print("Até mais...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()