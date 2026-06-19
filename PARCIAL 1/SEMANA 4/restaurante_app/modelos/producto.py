"""
Módulo que define la clase Producto para representar los artículos
que se ofrecen en el restaurante.
"""


class Producto:
    """
    Clase que representa un producto disponible en el restaurante.

    Atributos:
        id (int): Identificador único del producto
        nombre (str): Nombre del producto
        descripcion (str): Descripción del producto
        precio (float): Precio del producto
        categoria (str): Categoría del producto (plato, bebida, postre)
        disponible (bool): Indica si el producto está disponible
    """

    def __init__(self, id, nombre, descripcion, precio, categoria):
        """
        Inicializa una instancia de Producto.

        Args:
            id (int): Identificador único del producto
            nombre (str): Nombre del producto
            descripcion (str): Descripción del producto
            precio (float): Precio del producto
            categoria (str): Categoría del producto
        """
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.categoria = categoria
        self.disponible = True

    def get_id(self):
        """Retorna el ID del producto."""
        return self.id

    def get_nombre(self):
        """Retorna el nombre del producto."""
        return self.nombre

    def get_descripcion(self):
        """Retorna la descripción del producto."""
        return self.descripcion

    def get_precio(self):
        """Retorna el precio del producto."""
        return self.precio

    def get_categoria(self):
        """Retorna la categoría del producto."""
        return self.categoria

    def is_disponible(self):
        """Retorna si el producto está disponible."""
        return self.disponible

    def cambiar_disponibilidad(self, disponible):
        """
        Cambia el estado de disponibilidad del producto.

        Args:
            disponible (bool): Nuevo estado de disponibilidad
        """
        self.disponible = disponible

    def actualizar_precio(self, nuevo_precio):
        """
        Actualiza el precio del producto.

        Args:
            nuevo_precio (float): Nuevo precio del producto
        """
        if nuevo_precio > 0:
            self.precio = nuevo_precio
        else:
            print("Error: El precio debe ser mayor a 0")

    def __str__(self):
        """Retorna una representación en texto del producto."""
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Producto: {self.nombre} | Precio: ${self.precio:.2f} | Categoría: {self.categoria} | Estado: {estado}"

    def mostrar_informacion(self):
        """Muestra la información del producto de forma formateada."""
        estado = "Disponible" if self.disponible else "No disponible"
        print(f"\n{'='*50}")
        print(f"ID: {self.id}")
        print(f"Nombre: {self.nombre}")
        print(f"Descripción: {self.descripcion}")
        print(f"Precio: ${self.precio:.2f}")
        print(f"Categoría: {self.categoria}")
        print(f"Estado: {estado}")
        print(f"{'='*50}")

