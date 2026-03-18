import threading

def letras(letra):
    for i in range(5):
        print(f'Numero de Hilo {letra}')

hilos_abecedario = []
abcedario = ['a', 'b', 'c','d','e','f','g','h','i','j','k','l','m']

for letra in abcedario:
    hilo = threading.Thread(target=letras, args=(letra,))
    hilos_abecedario.append(hilo)
    hilo.start()

for hilo in hilos_abecedario:
    hilo.join()