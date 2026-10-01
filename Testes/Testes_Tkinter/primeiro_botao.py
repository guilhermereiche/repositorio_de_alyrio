import tkinter as tk

janela = tk.Tk()
janela.title("Meu primeiro botão")
janela.geometry("900x600")

def clicar():
    texto.config(text="Olá Guilherme, seja bem vindo ao seu aplicativo!")

def limpar():
    texto.config(text="Clique no botão abaixo")

texto = tk.Label(janela, text="Clique no botão abaixo")
texto.pack(pady=10)

botao = tk.Button(
    janela,
    text="Clique aqui",
    command=clicar
)

texto_limpar = tk.Label(janela, text="Clique aqui caso queira reiniciar o programa")


botao_limpar = tk.Button(
        janela,
        text="Clique para limpar",
        command=limpar
    )

botao.pack(pady=10)

texto_limpar.pack(pady=10)

botao_limpar.pack(pady=10)

janela.mainloop()