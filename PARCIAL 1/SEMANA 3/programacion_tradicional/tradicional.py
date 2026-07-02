"""Programa tradicional para registrar y mostrar información de una mascota.

Este archivo usa funciones y variables (no clases ni objetos) para:
- Solicitar datos al usuario
- Registrar los datos en un diccionario simple
- Mostrar la información de forma organizada
"""

def registrar_mascota():
	"""Solicita por teclado los datos de la mascota y devuelve un diccionario con la información."""
	print("Bienvenido a tu tienda de mascotas. Ingresa los datos de tu mascota")
	nombre = input("Ingrese el nombre de la mascota: ").strip()
	especie = input("Ingrese la especie (ej. perro, gato): ").strip()

	# Validar edad como entero
	while True:
		edad_input = input("Ingrese la edad (en años, número entero): ").strip()
		if edad_input.isdigit():
			edad = int(edad_input)
			break
		else:
			print("Edad inválida. Por favor ingrese un número entero (ej. 3).")

	sexo = input("Ingrese el sexo (M/F) [opcional]: ").strip()
	propietario = input("Ingrese el nombre del propietario [opcional]: ").strip()

	mascota = {
		'nombre': nombre,
		'especie': especie,
		'edad': edad,
		'sexo': sexo,
		'propietario': propietario,
	}
	return mascota


def mostrar_mascota(mascota):
	"""Recibe un diccionario con los datos de la mascota y los muestra ordenados."""
	print("\nInformación de la mascota registrada:")
	print("-" * 40)
	print(f"Nombre      : {mascota.get('nombre','')}")
	print(f"Especie     : {mascota.get('especie','')}")
	print(f"Edad (años) : {mascota.get('edad','')}")
	if mascota.get('sexo'):
		print(f"Sexo        : {mascota.get('sexo')}")
	if mascota.get('propietario'):
		print(f"Propietario : {mascota.get('propietario')}")
	print("-" * 40)


def main():
	mascota = registrar_mascota()
	mostrar_mascota(mascota)


if __name__ == '__main__':
	main()
