import pickle


class Auto:
    def __init__(self, modelo, placa):
        self.modelo = modelo
        self.placa = placa

    def __repr__(self):
        return f"El auto {self.modelo} tiene placa {self.placa}"


objeto_auto = Auto("Mazda", "ABC123")
objeto_auto1 = Auto("Mazda1", "ABC153")
objeto_auto2 = Auto("Mazda2", "ABC113")
objeto_auto3 = Auto("Mazda3", "ABC143")
objeto_auto4 = Auto("Mazda4", "ABC124")

autos = [objeto_auto, objeto_auto1, objeto_auto2, objeto_auto3, objeto_auto4]

# Esto guarda solo un objeto
# Escritura en autos.txt
with open("data.txt", "wb") as archivo:
    pickle.dump(autos, archivo)

# Lectura en autos.txt
with open("data.txt", "rb") as archivo:
    autos = pickle.load(archivo)

for auto in autos:
    print(auto)