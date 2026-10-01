import tkinter as tk

janela = tk.Tk()
janela.title("Contador")
janela.geometry("400x300")

numero = 0

def aumentar():
    global numero
    numero += 1
    contador.config(text=numero)

def diminuir():
    global numero
    numero -= 1
    contador.config(text=numero)

def zerar():
    global numero
    numero = 0
    contador.config(text=numero)

contador = tk.Label(janela, text="0", font=("Arial", 35))
contador.pack(pady=30)

botao1 = tk.Button(janela, text="+", command=aumentar)
botao1.pack(pady=10)

botao2 = tk.Button(janela, text="-", command=diminuir)
botao2.pack(pady=10)

botao3 = tk.Button(janela, text="Zerar contador", command=zerar)
botao3.pack(pady=10)

janela.mainloop()