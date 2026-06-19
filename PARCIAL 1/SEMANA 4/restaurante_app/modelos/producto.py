# Clase Producto - representa un plato, bebida o producto disponible en el restaurante

class Producto:
    """
    Representa un producto disponible en el restaurante LYDIA.
    Contiene información como nombre, tipo, precio y disponibilidad.
    """

    def __init__(self, nombre, tipo, precio, disponible=True):
        """
        Constructor de la clase Producto.

        Parámetros:
        - nombre: nombre del producto (str)
        - tipo: categoría del producto - 'plato', 'bebida', 'postre' (str)
        - precio: precio unitario del producto en dólares (float)
        - disponible: indicador de disponibilidad del producto (bool)
        """
        self.nombre = nombre
        self.tipo = tipo
        self.precio = precio
        self.disponible = disponible

    def __str__(self):
        """
        Retorna una representación en texto del producto.
        Muestra nombre, tipo, precio y estado de disponibilidad.
        """
        estado = "Disponible" if self.disponible else "No disponible"
        return f"[{self.tipo.upper()}] {self.nombre} - ${self.precio:.2f} ({estado})"

    def cambiar_disponibilidad(self, disponible):
        """
        Modifica el estado de disponibilidad del producto.

        Parámetro:
        - disponible: nuevo estado de disponibilidad (bool)
        """
        self.disponible = disponible
        return f"Disponibilidad de {self.nombre} actualizada a: {disponible}"

    def obtener_descripcion(self):
        """
        Retorna una descripción detallada del producto.
        """
        return f"Producto: {self.nombre}, Tipo: {self.tipo}, Precio: ${self.precio:.2f}"

