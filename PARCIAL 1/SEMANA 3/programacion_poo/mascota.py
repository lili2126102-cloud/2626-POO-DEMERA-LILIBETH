class Mascota:
    """Clase que representa una mascota.
    Atributos:
        nombre (str): Nombre de la mascota
        especie (str): Especie de la mascota (ej. 'perro', 'gato')
        edad (int): Edad en años

    Métodos:
        mostrar_informacion(): Imprime la información de la mascota
        hacer_sonido(): Imprime un sonido asociado a la especie
    """

    def __init__(self, nombre: str, especie: str, edad: int):
        self.nombre = nombre
        self.especie = especie.lower()
        self.edad = edad

    def mostrar_informacion(self) -> None:
        """Muestra en pantalla los atributos de la mascota."""
        print(f"Nombre: {self.nombre}")
        print(f"Especie: {self.especie}")
        print(f"Edad: {self.edad} años")

    def hacer_sonido(self) -> None:
        """Imprime un sonido representativo según la especie."""
        sonidos = {
            'perro': 'Guau guau! 🐶',
            'gato': 'Miau miau! 🐱',
            'pajaro': 'Pío pío! 🐦',
            'hamster': 'Chis chis! 🐹',
            'vaca': 'Muuu! 🐮',
        }
        sonido = sonidos.get(self.especie, '...sonido indefinido...')
        print(f"{self.nombre} hace: {sonido}")

    def __str__(self) -> str:
        return f"Mascota(nombre={self.nombre}, especie={self.especie}, edad={self.edad})"

