from Funcoes import *

while True:
    opcoes = input("=======MENU=======" + "\n"+
            "Digite I caso queira INSERIR um produto" + "\n"+
            "Digite P caso queira PESQUISAR sobre um produto" +"\n"+
            "Digite E caso queira EXCLUIR um produto" + "\n"+
            "QUAL A OPÇÃO SELECIONADA?: "
    ).upper()

    if opcoes == "I":
        inserir_produto()
    elif opcoes == "P":
        ...
    elif opcoes == "E":
        ...
    sair = input("Deseja sair? [S/N]").upper()
    if sair == "S":
        break
