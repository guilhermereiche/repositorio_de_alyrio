senha = "ReicheChefon"
contador = 3
while contador <= 3:
    tentativa = input("Digite a sua senha: ")
    if tentativa == senha:
        print("Você está dentro do programa!")
        break
    elif tentativa != senha:
        contador -= 1
        print("Senha incorreta, tente novamente")
        if contador == 0:
            print("Você esgotou suas tentativas e foi bloqueado, saindo do programa...")
            break

    print(f"Restam {contador} chances!")
    continue

