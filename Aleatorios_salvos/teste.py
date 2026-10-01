
resposta = input("Deseja entrar no programa?: ")
if resposta.lower() in ["s", "sim"]:
    while True:
        print("Olá, Mundo!")
        resposta2 = input("Deseja exibir a mensagem novamente? (s/n): ")
        if resposta2.lower() not in ["s", "sim"]:
            break
    print("Fim")

