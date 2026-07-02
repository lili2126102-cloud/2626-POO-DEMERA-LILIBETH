class Producto:
    """
    Clase padre que representa un producto general en el restaurante.
    Aplica encapsulación sobre el atributo crítico de precio.
    """
    def __init__(self, nombre: str, precio: float, disponible: bool = True):
        """
        Constructor de la clase Producto.
        
        :param nombre: Nombre del producto (e.g., "Hamburguesa", "Refresco").
        :param precio: Precio inicial del producto. Debe ser mayor que cero.
        :param disponible: Estado de disponibilidad en el menú (por defecto True).
        """
        self.nombre = nombre
        self.disponible = disponible
        
        # Atributo privado encapsulado con doble guion bajo
        self.__precio = 0.0
        
        # Asignamos el precio utilizando el método de modificación para validar el valor inicial
        self.cambiar_precio(precio)

    # Método de acceso (Getter)
    def obtener_precio(self) -> float:
        """
        Obtiene el precio actual del producto.
        
        :return: Valor flotante del precio.
        """
        return self.__precio

    # Método de modificación (Setter) con validación
    def cambiar_precio(self, nuevo_precio: float) -> bool:
        """
        Modifica el precio del producto aplicando reglas de validación.
        El precio no puede ser negativo ni igual a cero.
        
        :param nuevo_precio: Nuevo valor de precio propuesto.
        :return: True si el precio fue actualizado con éxito, False de lo contrario.
        """
        if nuevo_precio <= 0:
            print(f" ERROR: El precio de '{self.nombre}' no puede ser negativo o cero (Valor ingresado: {nuevo_precio}).")
            return False
        
        self.__precio = nuevo_precio
        return True

    def mostrar_informacion(self) -> None:
        """
        Muestra en consola la información básica del producto.
        """
        estado = "Disponible" if self.disponible else "No Disponible"
        print(f"Producto: {self.nombre}")
        print(f"  - Precio: ${self.obtener_precio():.2f}")
        print(f"  - Estado: {estado}")
