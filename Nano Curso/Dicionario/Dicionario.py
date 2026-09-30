usuarios = {}
print(usuarios)
usuarios = {
    "Chaves" : ["Chaves do 8", "24/12/2017", "Recep_01"],
    "Quico" : ["Quico das Flores", "20/12/2017", "Raiox_03"]
}
usuarios["Florinda"] = ["Dona Florinda", "24/12/2017", "Raiox_01"]
for usuario in usuarios:
    print(f"Nome do usuario: {usuario}")
    print(f"Valor do usuario: {usuarios[usuario]}")

print("Aqui são os valores atribuidos ao QUICO:", usuarios.get("Quico"))