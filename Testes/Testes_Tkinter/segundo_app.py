import tkinter as tk

janela = tk.Tk()
janela.title("Meu perfil")
janela.geometry("900x600")

titulo = tk.Label(janela, text="Meu perfil", font=("Times New Roman", 60, "bold"),fg='blue')
titulo.pack(pady=25)

nome = tk.Label(janela, text="Nome: Guilherme", font=("Arial", 15))
nome.pack()

idade = tk.Label(janela, text="Idade: 18 anos", font=("Arial", 15))
idade.pack()

curso = tk.Label(janela, text="Curso: Ciência da Computação", font=("Arial", 15))
curso.pack()

janela.mainloop()
