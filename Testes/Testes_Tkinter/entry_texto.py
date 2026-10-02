import tkinter as tk

janela = tk.Tk()
janela.title("Cadastro")
janela.geometry("400x300")

def mostrar_nome():
    nome = campo.get()
    if nome == "Enzo Guislandi":
        resultado.config(text="Oxi, o fiote entrou no programa?")
    elif nome == "Guilherme Reiche":
        resultado.config(text="Olá, Big Boss Chefon e Scrum Master!")
    else:
        resultado.config(text=f"Olá, {nome}!")

def limpar_resultado():
    resultado.config(text="")

titulo = tk.Label(janela, text="Digite seu nome:")
titulo.pack(pady=20)

campo = tk.Entry(janela)
campo.pack()

botao = tk.Button(janela, text="Enviar", command=mostrar_nome)
botao.pack(pady=15)



resultado = tk.Label(janela, text="")
resultado.pack()

excluir_resultado = tk.Button(janela, text="Excluir resultado", command=limpar_resultado)
excluir_resultado.pack(pady=10)

janela.mainloop()