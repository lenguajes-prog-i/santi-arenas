# Control de parqueaderos

import threading
import time
# import random
from random import randint

sem = threading.Semaphore(3)

def carro(id):
    print(f"carro {id} intentando entrar...")

    with sem:
        print(f"Carro {id} ha entrado al parqueadero")
        tiempo = randint(1,3)
        time.sleep(tiempo)
        print(f"Carro {id} sale con tiempo de {tiempo} segundos")

hilos = []

for i in range(10):
    hi = threading.Thread(target=carro, args=(i,))
    hilos.append(hi)
    hi.start()

for h in hilos:
    h.join()


print("------------Parqueadero Libre-------------")
