# -*- coding: utf-8 -*-

class Producto:
    """
    Clase que representa un producto del restaurante.
    Aplica encapsulación mediante decoradores @property y @setter para
    controlar el acceso y modificación de sus atributos con validaciones.
    """

    def __init__(self, nombre: str, categoria: str, precio: float, disponible: bool = True):
        """
        Constructor tradicional de la clase Producto.
        Al asignar los valores a través de self.nombre, self.categoria, etc.,
        se invocan automáticamente los setters correspondientes, ejecutando las validaciones.
        """
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.disponible = disponible

    # --- Propiedad: nombre ---
    @property
    def nombre(self) -> str:
        """Getter para obtener el nombre del producto."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Setter para validar y asignar el nombre del producto."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = valor.strip()

    # --- Propiedad: categoria ---
    @property
    def categoria(self) -> str:
        """Getter para obtener la categoría del producto."""
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        """Setter para validar y asignar la categoría del producto."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La categoría del producto no puede estar vacía.")
        self._categoria = valor.strip()

    # --- Propiedad: precio ---
    @property
    def precio(self) -> float:
        """Getter para obtener el precio del producto."""
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        """Setter para validar y asignar el precio del producto."""
        try:
            valor_num = float(valor)
        except (ValueError, TypeError):
            raise ValueError("El precio debe ser un valor numérico válido.")
        
        if valor_num <= 0:
            raise ValueError("El precio del producto debe ser mayor que cero.")
        self._precio = valor_num

    # --- Propiedad: disponible ---
    @property
    def disponible(self) -> bool:
        """Getter para obtener la disponibilidad del producto."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        """Setter para asignar la disponibilidad del producto."""
        # Nos aseguramos de guardarlo como booleano
        self._disponible = bool(valor)

    def mostrar_informacion(self) -> None:
        """
        Muestra en consola la información del producto de forma legible y formateada.
        """
        estado = "Disponible" if self.disponible else "No Disponible"
        print(f"Producto: {self.nombre}")
        print(f"  - Categoría: {self.categoria}")
        print(f"  - Precio: ${self.precio:.2f}")
        print(f"  - Estado: {estado}")
