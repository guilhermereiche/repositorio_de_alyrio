class Disciplina:
    def __init__(self, nome, professor):
        self.nome = nome
        self.professor = professor

    def exibir_infos(self):
        print(f"Disciplina: {self.nome} | Professor: {self.professor}")

# Temporario
# prompt_ia = Disciplina("Prompt & IA", "Jorge")
# prompt_ia.exibir_infos()
#
# python_automacao = Disciplina("Automacao com Python", "Russi")
# python_automacao.exibir_infos()
