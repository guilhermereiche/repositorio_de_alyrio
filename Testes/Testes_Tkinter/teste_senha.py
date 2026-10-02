import tkinter as tk

janela = tk.Tk()
janela.title("Cadastro com senha")
janela.geometry("900x600")

# MOSTRA O TÍTULO DO PROGRAMA
titulo = tk.Label(
    janela,
    text="Digite sua senha:",
    font=("Arial", 15)
    )

titulo.pack(pady=15)

# CRIA O ENTRY PRA DIGITAR A SENHA
input_senha = tk.Entry(janela)
input_senha.pack(pady=10)

# CRIA O BOTÃO PRA SUBMETER A SENHA
# botao_senha = tk.Button(janela, text="Enviar")
# botao_senha.pack(pady=10)

# PROGRAMA DA SENHA
senha_correta = "Gui240907"
contador = 3

def validacao_senha():
    global contador

    resultado = input_senha.get()

    if resultado not in senha_correta :
        mensagem_final.config(text="Senha incorreta!!")
        limite_esgotado = tk.Label(janela, text=f"Você tem mais {contador-1} tentativas!")
        limite_esgotado.pack(pady=10)
        contador -= 1

        if contador == 0:
            limite_esgotado.config(text="Tentativas esgotadas!")
            resultado_print.config(state="disabled")

    elif resultado == "Gui240907":
        mensagem_final.config(text="Você está cadastrado!")
        mensagem_final.pack(pady=10)


resultado_print = tk.Button(janela,text="Enviar", command=validacao_senha)
resultado_print.pack(pady=10)

mensagem_final = tk.Label(janela, text="")
mensagem_final.pack()


janela.mainloop()