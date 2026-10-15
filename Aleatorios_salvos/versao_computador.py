import platform
from datetime import datetime

print("Nome da maquina: ", platform.node())
print("Arquitetura: ", platform.architecture())
print("Versao: ", platform.release())
print("Sistera Operaciomal: ", platform.system())
print("Processador: ", platform.processor())
print("Versao do python: ", platform.python_version())

print(datetime.now())