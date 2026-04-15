import pickle

autos = [
    {"modelo": "Mazda", "placa": "ABC123"},
    {"modelo": "Mazda1", "placa": "ABC153"},
    {"modelo": "Mazda2", "placa": "ABC113"},
    {"modelo": "Mazda3", "placa": "ABC143"},
    {"modelo": "Mazda4", "placa": "ABC124"}
]

def guardar_autos(autos, nombre_archivo):
    with open(nombre_archivo, "wb") as archivo:
        pickle.dump(autos, archivo)


def cargar_autos(nombre_archivo):
    with open(nombre_archivo, "rb") as archivo:
        return pickle.load(archivo)
    
def mostrar_autos(autos):
    list(map(lambda auto: print(f"El auto {auto['modelo']} tiene placa {auto['placa']}"), autos))

nombre_archivo = "data.txt"
guardar_autos(autos, nombre_archivo)
autos_cargados = cargar_autos(nombre_archivo)
mostrar_autos(autos_cargados)