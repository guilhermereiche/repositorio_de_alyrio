times = input("Quais times você conhece?: ")
if times in ["Atlético Mineiro", "Bahia", "Botafogo", "Ceará", "Corinthians", "Cruzeiro", "Flamengo", "Fluminense", "Fortaleza", "Grêmio", "Internacional", "Juventude", "Mirassol", "Palmeiras", "Red Bull Bragantino", "Santos", "Sport Recife", "São Paulo", "Vasco da Gama", "Vitória", "América Mineiro", "Amazonas", "Athletico Paranaense", "Atlético Goianiense", "Avaí", "Botafogo de Ribeirão Preto", "Chapecoense", "Coritiba", "CRB", "Criciúma", "Cuiabá", "Ferroviária", "Goiás", "Novorizontino", "Operário Ferroviário", "Paysandu", "Remo", "Vila Nova", "Volta Redonda", "Athletic Club"]:
    while True:
        print("Você conhece muitos times!")
        if times == "Corinthians":
            print("AQUI É CORINGAO PORRA!")
        times2 = input("Digite outro time: ")
        if times2 not in ["Atlético Mineiro", "Bahia", "Botafogo", "Ceará", "Corinthians", "Cruzeiro", "Flamengo", "Fluminense", "Fortaleza", "Grêmio", "Internacional", "Juventude", "Mirassol", "Palmeiras", "Red Bull Bragantino", "Santos", "Sport Recife", "São Paulo", "Vasco da Gama", "Vitória", "América Mineiro", "Amazonas", "Athletico Paranaense", "Atlético Goianiense", "Avaí", "Botafogo de Ribeirão Preto", "Chapecoense", "Coritiba", "CRB", "Criciúma", "Cuiabá", "Ferroviária", "Goiás", "Novorizontino", "Operário Ferroviário", "Paysandu", "Remo", "Vila Nova", "Volta Redonda"]:
            print("Esse time não é tão conhecido assim!")
            break