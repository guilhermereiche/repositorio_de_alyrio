resposta = input("Deseja entrar no programa?: ")
if resposta.lower() in ["sim", "s"]:
    while True:
        print("Olá, Mundo!")
        resposta2 = input("Deseja entrar novamente no programa?: ")
        if resposta2.lower() not in ["sim", "s"]:

            print("Interação finalizada!")
            break