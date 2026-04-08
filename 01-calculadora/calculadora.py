numero1 = float(input("Ingrese el primer número: "))
numero2 = float(input("Ingrese el segundo número: "))


print("Seleccione la operación:")
print("1. Suma")
print("2. Resta")
print("3. Multiplicación")
print("4. División")
op = input("Ingrese el número de la operación que desea realizar: ")

if op == "1":
    resultado = numero1 + numero2
    print(f"El resultado de la suma es: {resultado}")
elif op == "2":
    resultado = numero1 - numero2
    print(f"El resultado de la resta es: {resultado}")
elif op == "3":
    resultado = numero1 * numero2
    print(f"El resultado de la multiplicación es: {resultado}")
elif op == "4":
    if numero2 != 0:
        resultado = numero1 / numero2
        print(f"El resultado de la división es: {resultado}")
    else:
        print("Error: No se puede dividir por cero.")
else:
    print("Operación no válida.")