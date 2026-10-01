# Exercício 1
# Calcule a área de um círculo com raio 5. Use a fórmula: área = π * raio^2. 
# (Dica: você pode usar 3.14159 como valor aproximado de π).

r = float(input("Digite o raio: "))
área = float(3.14159 * r**2)
print(round(área,1))

# Exercício 2
# Converta uma temperatura de Fahrenheit para Celsius. 
#A fórmula de conversão é: Celsius = (Fahrenheit - 32) * 5/9

F = float(input("Digite a temperatura em Fahrenheit: ")) 
C = (F - 32) * 5/9
print(f"Essa é a temperatura em Graus Celsius: {round(C,1)}")

# Exercício 3 
#Você comprou 3 livros por R$ 25 cada e 2 canetas por R$ 5 cada. 
#Calcule o total gasto.
Livro = int(input("Quantos livros você comprou?: "))
Caneta = int(input("Quantas canetas você comprou?: "))
Total = (Livro * 25 + Caneta * 5)
print(f"O total gasto foi de R$ {Total}")

# Exercício 4
Velocidade = float(input("Qual a velocidade média do carro?: "))
Distância = float(input("Qual a distância percorrida?: "))
Tempo = (Distância/Velocidade)
print(f"O carro levou {round(Tempo,2)} horas para percorrer essa distância")

# Exercício 5
Nota_1 = float(input("Qual sua primeira nota?: "))
Nota_2 = float(input("Qual sua segunda nota?: "))
Média = float((Nota_1 + Nota_2) / 2)
print(f"Sua média é de {round(Média,1)}")

#Exercício 6
Nota_1 = float(input("Qual sua primeira nota?: "))
Nota_2 = float(input("Qual sua segunda nota?: "))
Média = float((Nota_1*4 + Nota_2*6) / (4+6))
print(f"Sua média é de {round(Média,1)}")

# Exercício 7
#Preço da peça1 = R$ 25.00
#Preço da peça2 = R$ 12.00

peça1 = float(input("Quantas peças1 você quer?: "))
peça2 = float(input("Quantas peças2 você quer?: "))
Total = float(peça1*25 + peça2*12)
print(f"O valor a ser pago é de {round(Total,2)}")

#Exercício 8
Valor_recebido = float(input("Qual foi o valor recebido?: "))
Valor_produto = float(input("Qual é o valor do produto?: "))
Troco = float(Valor_recebido - Valor_produto)
print(f"Seu troco é de {round(Troco,2)}")