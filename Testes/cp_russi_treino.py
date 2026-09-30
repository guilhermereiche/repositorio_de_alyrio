from statistics import median

temperaturas = [[28, 31, 34, 33],
                [25, 27, 29, 28],
                [32, 35, 36, 34],
                [24, 26, 25, 27]]
sala = 1
maior_risco = 0
sala_maior_risco = 0
for temperatura in temperaturas:
    print("Sala: ",sala)
    reg_crit = 0
    for temp_sala in temperatura:
        media = float(sum(temperatura) / len(temperatura))
        if temp_sala >= 33:
            reg_crit += 1

    print("Média:",media)
    print("Registros Críticos:", reg_crit)
    print()

    if reg_crit>maior_risco:
        maior_risco = reg_crit
        sala_maior_risco = sala
    sala += 1
print("Sala com maior risco: Sala", sala_maior_risco)