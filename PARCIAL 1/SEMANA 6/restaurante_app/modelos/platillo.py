from modelos.producto import Producto

class Platillo(Producto):
    """
    Clase hija que representa un platillo o comida del restaurante.
    Hereda de la clase Producto y añade el atributo calorías.
    """
    def __init__(self, nombre: str, precio: float, disponible: bool, calorias: int):
        """
        Constructor de la clase Platillo.
        
        :param nombre: Nombre del platillo.
        :param precio: Precio del platillo.
        :param disponible: Estado de disponibilidad.
        :param calorias: Cantidad de calorías en kilocalorías (kcal).
        """
        # Llamada al constructor de la clase padre mediante super()
        super().__init__(nombre, precio, disponible)
        self.calorias = calorias

    def mostrar_informacion(self) -> None:
        """
        Sobrescribe el método mostrar_informacion de la clase padre
        para incluir la información específica de un platillo.
        """
        # Podemos llamar al método mostrar_informacion() de la clase padre
        # o formatearlo de forma personalizada. Para una salida limpia y organizada,
        # llamamos a la base y agregamos el atributo exclusivo.
        super().mostrar_informacion()
        print(f"  - Calorías: {self.calorias} kcal")
        print("-" * 30)
