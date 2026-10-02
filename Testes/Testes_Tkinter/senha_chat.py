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

# PROGRAMA DA SENHA
senha_correta = "Gui240907"
contador = 3

def validacao_senha():
    global contador

    resultado = input_senha.get()

    if contador <= 0:
        mensagem_final.config(text="Limite de tentativas atingido!")
        resultado_print.config(state="disabled")

    elif resultado == senha_correta:
        mensagem_final.config(text="Você está cadastrado!")
        resultado_print.config(state="disabled")

    else:
        contador -= 1
        mensagem_final.config(
            text=f"Senha incorreta! Você tem {contador} tentativas."
        )

        if contador == 0:
            mensagem_final.config(text="Limite de tentativas atingido!")
            resultado_print.config(state="disabled")

# CRIA O BOTÃO
resultado_print = tk.Button(
    janela,
    text="Enviar",
    command=validacao_senha
)
resultado_print.pack(pady=10)

# MOSTRA O RESULTADO
mensagem_final = tk.Label(janela, text="")
mensagem_final.pack(pady=10)

janela.mainloop()