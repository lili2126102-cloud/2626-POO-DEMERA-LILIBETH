# -*- coding: utf-8 -*-

class Venta:
    """
    Clase que representa una venta realizada en el restaurante.
    Relaciona a un usuario (mediante su ID/identificación) con un producto
    (mediante su código) y la cantidad vendida.
    """

    def __init__(self, usuario_id: str, producto_codigo: str, cantidad: int) -> None:
        """
        Constructor de la clase Venta.
        Inicializa los atributos mediante sus setters para validar la información.
        """
        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.cantidad = cantidad

    # --- Propiedad: usuario_id ---
    @property
    def usuario_id(self) -> str:
        """Getter para obtener el identificador del usuario."""
        return self._usuario_id

    @usuario_id.setter
    def usuario_id(self, valor: str) -> None:
        """Setter para validar y asignar el ID del usuario."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El ID del usuario no puede estar vacío.")
        self._usuario_id = valor.strip()

    # --- Propiedad: producto_codigo ---
    @property
    def producto_codigo(self) -> str:
        """Getter para obtener el código del producto."""
        return self._producto_codigo

    @producto_codigo.setter
    def producto_codigo(self, valor: str) -> None:
        """Setter para validar y asignar el código del producto."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        self._producto_codigo = valor.strip()

    # --- Propiedad: cantidad ---
    @property
    def cantidad(self) -> int:
        """Getter para obtener la cantidad vendida."""
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        """Setter para validar y asignar la cantidad, asegurando que sea mayor que cero."""
        try:
            valor_num = int(valor)
        except (ValueError, TypeError):
            raise ValueError("La cantidad vendida debe ser un número entero válido.")
        
        if valor_num <= 0:
            raise ValueError("La cantidad vendida debe ser estrictamente mayor que cero.")
        self._cantidad = valor_num

    def to_dict(self) -> dict:
        """
        Convierte el objeto Venta en un diccionario para serialización JSON.
        """
        return {
            "usuario_id": self.usuario_id,
            "producto_codigo": self.producto_codigo,
            "cantidad": self.cantidad
        }

    @classmethod
    def from_dict(cls, datos: dict) -> 'Venta':
        """
        Reconstruye un objeto Venta a partir de un diccionario de datos.
        Lanza KeyError si falta alguna de las claves esperadas.
        Lanza ValueError si los datos no pasan las validaciones de la clase.
        """
        for clave in ["usuario_id", "producto_codigo", "cantidad"]:
            if clave not in datos:
                raise KeyError(f"Clave faltante '{clave}' en los datos de la venta.")
        
        return cls(
            usuario_id=datos["usuario_id"],
            producto_codigo=datos["producto_codigo"],
            cantidad=datos["cantidad"]
        )
