user = "adminsan@uniremington.edu.co"
password = "santy123"

user_input = input("Ingrese su correo electronico: ")
password_input = input("Ingrese su contraseña: ")

if user_input == user and password_input == password:
    print("Inicio de sesión exitoso.")
else:
    print("Correo electrónico o contraseña incorrectos.")