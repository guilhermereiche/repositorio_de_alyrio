from aluno import Aluno
from disciplina import Disciplina

# criar / instanciar 1 aluno
aluno1 = Aluno("João", "123456", "Ciência da Computação")

# criar / instanciar 2 disciplinas
sers = Disciplina("Soluções Renováveis", "André")
dsa = Disciplina("Data Structures", "Erick")

# Matricular o aluno nas disciplinas

aluno1.matricular(sers)
aluno1.matricular(dsa)
print(aluno1.disciplinas[0].professor)

# Atribuir a(s) notas de cada disciplina ao aluno
aluno1.adicionar_nota(sers, 10)
aluno1.adicionar_nota(sers, 8)
aluno1.adicionar_nota(dsa, 5)
aluno1.adicionar_nota(dsa, 3)