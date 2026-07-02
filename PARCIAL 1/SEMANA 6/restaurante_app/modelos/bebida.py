from modelos.producto import Producto

class Bebida(Producto):
    """
    Clase hija que representa una bebida en el restaurante.
    Hereda de la clase Producto y añade el atributo volumen.
    """
    def __init__(self, nombre: str, precio: float, disponible: bool, volumen: int):
        """
        Constructor de la clase Bebida.
        
        :param nombre: Nombre de la bebida.
        :param precio: Precio de la bebida.
        :param disponible: Estado de disponibilidad.
        :param volumen: Volumen de la bebida en mililitros (ml).
        """
        # Llamada al constructor de la clase padre mediante super()
        super().__init__(nombre, precio, disponible)
        self.volumen = volumen

    def mostrar_informacion(self) -> None:
        """
        Sobrescribe el método mostrar_informacion de la clase padre
        para incluir la información específica de una bebida.
        """
        super().mostrar_informacion()
        print(f"  - Volumen: {self.volumen} ml")
        print("-" * 30)
