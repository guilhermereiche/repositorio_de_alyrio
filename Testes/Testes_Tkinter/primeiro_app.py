import tkinter as tk

janela = tk.Tk()

janela.title("Meu aplicativo")
janela.geometry("1000x700")
janela.configure(bg="#202020")
janela.resizable(False, False)

texto = tk.Label(
    janela,
    text="Seja bem vindo, Enzo Giodick!",
    font=("Times New Roman", 35, "bold"),
    bg="#202020",
    fg="brown"
)

texto.pack(pady=100)

janela.mainloop()