"""Módulo que define la clase Mascota.

La clase muestra uso de clase, objeto, atributos, métodos y abstracción.
"""

class Mascota:
	"""Representa una mascota con nombre, especie y edad.

	Atributos:
		nombre (str): Nombre de la mascota.
		especie (str): Especie de la mascota (ej. 'perro', 'gato').
		edad (int): Edad en años.
	"""

	def __init__(self, nombre: str, especie: str, edad: int) -> None:
		self.nombre = nombre
		self.especie = especie.lower()
		self.edad = edad

	def mostrar_informacion(self) -> str:
		"""Devuelve una cadena con la información de la mascota.

		Este método ejemplifica el encapsulamiento y presentación de datos
		a través de un método de instancia.
		"""
		return f"Nombre: {self.nombre} | Especie: {self.especie} | Edad: {self.edad} años"

	def hacer_sonido(self) -> str:
		"""Devuelve el sonido que hace la mascota según su especie.

		Implementa una abstracción simple: no hace falta conocer cómo se
		determina el sonido, sólo usar el método.
		"""
		sonidos = {
			'perro': '¡Guau! 🐶',
			'gato': '¡Miau! 🐱',
			'pajaro': '¡Pío! 🐦',
			'pez': '... (silencio, un pez no hace sonido audible)',
		}
		return sonidos.get(self.especie, 'Sonido desconocido')

	def __str__(self) -> str:  # Representación amigable
		return self.mostrar_informacion()


