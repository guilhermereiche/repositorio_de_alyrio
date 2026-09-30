NOME_MISSAO = "Orion Test Alpha"
NOME_EQUIPE = "Equipe Apollo"

dados_missao = [
    [24, 92, 88, 96, 90], # Ciclo 1
    [27, 80, 72, 94, 85], # Ciclo 2
    [31, 65, 58, 91, 70], # Ciclo 3
    [36, 42, 38, 87, 55], # Ciclo 4
    [39, 28, 19, 78, 35], # Ciclo 5
    [34, 55, 32, 82, 50]  # Ciclo 6
]

areas_monitoradas = [
    "Temperatura interna",
    "Comunicação com a base",
    "Sistema de energia",
    "Suporte de oxigênio",
    "Estabilidade operacional"
]

unidades = ["°C", "%", "%", "%", "%"]

def analisar_temperatura(valor):

    if valor < 18:
        return "ATENÇÃO", 1, "Temperatura abaixo do ideal"
    elif valor <= 30:
        return "NORMAL", 0, "Temperatura estável"
    elif valor <= 35:
        return "ATENÇÃO", 1, "Temperatura elevada"
    else:
        return "CRÍTICO", 2, "Risco de superaquecimento"


def analisar_comunicacao(valor):

    if valor < 30:
        return "CRÍTICO", 2, "Comunicação com a base em nível crítico"
    elif valor < 60:
        return "ATENÇÃO", 1, "Comunicação instável"
    else:
        return "NORMAL", 0, "Comunicação estável"


def analisar_bateria(valor):

    if valor < 20:
        return "CRÍTICO", 2, "Bateria em nível crítico"
    elif valor < 50:
        return "ATENÇÃO", 1, "Bateria abaixo do recomendado"
    else:
        return "NORMAL", 0, "Energia estável"


def analisar_oxigenio(valor):

    if valor < 80:
        return "CRÍTICO", 2, "Oxigênio em nível crítico"
    elif valor < 90:
        return "ATENÇÃO", 1, "Oxigênio abaixo do ideal"
    else:
        return "NORMAL", 0, "Oxigênio adequado"


def analisar_estabilidade(valor):

    if valor < 40:
        return "CRÍTICO", 2, "Estabilidade operacional crítica"
    elif valor < 70:
        return "ATENÇÃO", 1, "Estabilidade operacional reduzida"
    else:
        return "NORMAL", 0, "Estabilidade operacional adequada"

def classificar_ciclo(pontuacao):

    if pontuacao <= 2:
        return "MISSÃO ESTÁVEL"
    elif pontuacao <= 5:
        return "MISSÃO EM ATENÇÃO"
    else:
        return "MISSÃO CRÍTICA"


def gerar_recomendacao(resultados):

    criticos = []
    atencoes = []

    for i, (classificacao, _, _) in enumerate(resultados):
        if classificacao == "CRÍTICO":
            criticos.append(i)
        elif classificacao == "ATENÇÃO":
            atencoes.append(i)

    recomendacoes = {
        0: "Verificar controle térmico da missão.",
        1: "Tentar restabelecer contato com a base.",
        2: "Ativar modo de economia de energia.",
        3: "Acionar protocolo de suporte à vida.",
        4: "Reduzir operações não essenciais."
    }

    if len(criticos) >= 3:
        return "Ativar modo de segurança e priorizar suporte à vida, energia e comunicação."
    elif len(criticos) > 0:
        return recomendacoes[criticos[0]]
    elif len(atencoes) > 0:
        return "Monitorar sistemas em atenção e preparar plano de contingência."
    else:
        return "Manter operação normal e continuar monitoramento."


def analisar_tendencia(risco_primeiro, risco_ultimo):

    if risco_ultimo > risco_primeiro:
        return "A missão apresentou tendência de piora."
    elif risco_ultimo < risco_primeiro:
        return "A missão apresentou tendência de melhora."
    else:
        return "A missão permaneceu estável em relação ao início."


def identificar_area_mais_afetada(pontuacoes_areas):

    max_pontuacao = max(pontuacoes_areas)
    indices_max = [i for i, p in enumerate(pontuacoes_areas) if p == max_pontuacao]

    if len(indices_max) == 1:
        return areas_monitoradas[indices_max[0]], pontuacoes_areas[indices_max[0]]
    else:
        areas_empate = [areas_monitoradas[i] for i in indices_max]
        return ", ".join(areas_empate), max_pontuacao


def gerar_relatorio_final(dados, resultados_ciclos, pontuacoes_areas, risco_primeiro, risco_ultimo):

    num_ciclos = len(dados)

    medias = []
    for col in range(5):
        soma = sum(dados[ciclo][col] for ciclo in range(num_ciclos))
        medias.append(soma / num_ciclos)

    pontuacoes = [r["pontuacao"] for r in resultados_ciclos]
    max_pontuacao = max(pontuacoes)
    ciclo_mais_critico = pontuacoes.index(max_pontuacao) + 1

    risco_medio = sum(pontuacoes) / num_ciclos

    ciclos_criticos = sum(1 for p in pontuacoes if p >= 6)

    tendencia = analisar_tendencia(risco_primeiro, risco_ultimo)

    area_mais_afetada, pontuacao_max = identificar_area_mais_afetada(pontuacoes_areas)

    classificacao_final = classificar_ciclo(round(risco_medio))

    if classificacao_final == "MISSÃO ESTÁVEL":
        conclusao = "A missão foi concluída com sucesso. Todos os sistemas operaram dentro dos parâmetros normais."
    elif classificacao_final == "MISSÃO EM ATENÇÃO":
        conclusao = "A missão apresentou instabilidade relevante durante a operação. Apesar da tentativa de recuperação no último ciclo, ainda existem sistemas em atenção e a equipe deve manter o plano de contingência ativo."
    else:
        conclusao = "A missão enfrentou condições críticas significativas. Recomenda-se análise detalhada de todos os sistemas e revisão dos protocolos de segurança."

    print("=" * 60)
    print("RELATÓRIO FINAL DA MISSÃO")
    print("=" * 60)
    print(f"Missão: {NOME_MISSAO}")
    print(f"Equipe: {NOME_EQUIPE}")
    print(f"Quantidade de ciclos analisados: {num_ciclos}")
    print("-" * 60)

    print(f"Média de temperatura: {medias[0]:.2f} °C")
    print(f"Média de comunicação: {medias[1]:.2f}%")
    print(f"Média de bateria: {medias[2]:.2f}%")
    print(f"Média de oxigênio: {medias[3]:.2f}%")
    print(f"Média de estabilidade: {medias[4]:.2f}%")
    print("-" * 60)

    print(f"Ciclo mais crítico: Ciclo {ciclo_mais_critico}")
    print(f"Maior pontuação de risco: {max_pontuacao}")
    print(f"Risco médio da missão: {risco_medio:.2f}")
    print(f"Quantidade de ciclos críticos: {ciclos_criticos}")
    print("-" * 60)

    print("Tendência da missão:")
    print(tendencia)
    print("-" * 60)

    print("Pontuação acumulada por área:")
    for i, area in enumerate(areas_monitoradas):
        print(f"{area}: {pontuacoes_areas[i]} pontos")
    print("-" * 60)

    print("Área mais afetada:")
    print(area_mais_afetada)
    print("-" * 60)

    print("Classificação final da missão:")
    print(classificacao_final)
    print("-" * 60)

    print("Conclusão:")
    print(conclusao)
    print("=" * 60)

def executar_sistema():

    funcoes_analise = [
        analisar_temperatura,
        analisar_comunicacao,
        analisar_bateria,
        analisar_oxigenio,
        analisar_estabilidade
    ]

    resultados_ciclos = []

    pontuacoes_areas = [0, 0, 0, 0, 0]

    print("=" * 60)
    print("MISSION CONTROL AI")
    print("=" * 60)
    print(f"Missão: {NOME_MISSAO}")
    print(f"Equipe: {NOME_EQUIPE}")
    print(f"Quantidade de ciclos analisados: {len(dados_missao)}")
    print("=" * 60)

    for ciclo_idx, ciclo_dados in enumerate(dados_missao):
        print(f"\nCICLO {ciclo_idx + 1}")
        print("-" * 60)

        resultados_ciclo = []
        pontuacao_ciclo = 0

        for param_idx, valor in enumerate(ciclo_dados):
            classificacao, pontuacao, mensagem = funcoes_analise[param_idx](valor)
            resultados_ciclo.append((classificacao, pontuacao, mensagem))
            pontuacao_ciclo += pontuacao
            pontuacoes_areas[param_idx] += pontuacao

            print(f"{areas_monitoradas[param_idx]}: {valor}{unidades[param_idx]} | {classificacao} | {mensagem}")

        classificacao_ciclo = classificar_ciclo(pontuacao_ciclo)
        recomendacao = gerar_recomendacao(resultados_ciclo)

        print(f"\nPontuação de risco do ciclo: {pontuacao_ciclo}")
        print(f"Classificação do ciclo: {classificacao_ciclo}")
        print(f"Recomendação: {recomendacao}")

        resultados_ciclos.append({
            "resultados": resultados_ciclo,
            "pontuacao": pontuacao_ciclo,
            "classificacao": classificacao_ciclo,
            "recomendacao": recomendacao
        })

    risco_primeiro = resultados_ciclos[0]["pontuacao"]
    risco_ultimo = resultados_ciclos[-1]["pontuacao"]

    gerar_relatorio_final(dados_missao, resultados_ciclos, pontuacoes_areas, risco_primeiro, risco_ultimo)

if __name__ == "__main__":
    executar_sistema()