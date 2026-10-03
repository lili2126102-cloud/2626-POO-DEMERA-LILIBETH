
"""Programa principal que crea objetos de la clase Mascota y muestra su información.

Se crean al menos dos objetos y se ejecutan los métodos definidos en la clase.
"""

from mascota import Mascota


def main() -> None:
	# Crear al menos dos mascotas
	mascota1 = Mascota("Firulais", "Perro", 4)
	mascota2 = Mascota("Misu", "Gato", 2)
	mascota3 = Mascota("Nemo", "Pez", 1)  # opcional, tercer objeto

	mascotas = [mascota1, mascota2, mascota3]

	# Ejecutar métodos y mostrar información
	for m in mascotas:
		print(m.mostrar_informacion())
		print("-> Sonido:", m.hacer_sonido())
		print('-' * 40)


if __name__ == '__main__':
	main()

