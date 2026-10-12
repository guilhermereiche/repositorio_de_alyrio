arquivo = open("primeiro_arquivo.txt", "w")

arquivo.write("\nMeu primeiro arquivo! Que felicidade!")

arquivo.close()

with open('primeiro_arquivo.txt', 'a') as arquivo:
    arquivo.write("\nEu amo Jesus Cristo!"
                  "\nSou o Guilherme Reiche"
                  "\nAqui eh Corinthians!")

with open('primeiro_arquivo.txt', 'r') as arquivo:
    conteudo = arquivo.readline()
    for linha in arquivo:
        print(linha)