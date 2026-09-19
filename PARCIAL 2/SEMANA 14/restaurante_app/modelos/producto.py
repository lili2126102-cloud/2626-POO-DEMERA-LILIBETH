# -*- coding: utf-8 -*-
"""
Modelo de Producto - Restaurante App (Semana 14)
================================================
Representa un producto del catálogo del restaurante con validaciones estrictas
mediante propiedades encapsuladas (@property y @setter).
"""


class Producto:
    """
    Entidad que representa un plato, bebida o postre del restaurante.
    Aplica encapsulación rigurosa para garantizar la integridad de los datos:
    - Código no vacío
    - Nombre no vacío
    - Categoría no vacía
    - Precio numérico estrictamente positivo (> 0)
    - Stock entero no negativo (>= 0)
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int = 0
    ) -> None:
        """
        Inicializa un producto validando todos sus campos a través de sus setters.
        """
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    # --- Propiedad: codigo ---
    @property
    def codigo(self) -> str:
        """Getter para el código único del producto."""
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        """Setter con validación de código no vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        self._codigo = valor.strip().upper()

    # --- Propiedad: nombre ---
    @property
    def nombre(self) -> str:
        """Getter para el nombre del producto."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Setter con validación de nombre no vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = valor.strip()

    # --- Propiedad: categoria ---
    @property
    def categoria(self) -> str:
        """Getter para la categoría del producto."""
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        """Setter con validación de categoría no vacía."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La categoría del producto no puede estar vacía.")
        self._categoria = valor.strip()

    # --- Propiedad: precio ---
    @property
    def precio(self) -> float:
        """Getter para el precio unitario del producto."""
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        """Setter con validación de precio numérico positivo (> 0)."""
        try:
            valor_num = float(valor)
        except (ValueError, TypeError):
            raise ValueError("El precio debe ser un valor numérico válido.")

        if valor_num <= 0:
            raise ValueError("El precio del producto debe ser estrictamente mayor que cero.")
        self._precio = round(valor_num, 2)

    # --- Propiedad: stock ---
    @property
    def stock(self) -> int:
        """Getter para el stock o inventario disponible."""
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        """Setter con validación de stock entero no negativo (>= 0)."""
        try:
            valor_num = int(valor)
        except (ValueError, TypeError):
            raise ValueError("El stock debe ser un número entero válido.")

        if valor_num < 0:
            raise ValueError("El stock del producto no puede ser negativo.")
        self._stock = valor_num

    def to_dict(self) -> dict:
        """Convierte el objeto Producto en un diccionario para persistencia JSON."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock
        }

    @classmethod
    def from_dict(cls, datos: dict) -> 'Producto':
        """
        Reconstruye un objeto Producto a partir de un diccionario de datos.
        Lanza KeyError si falta alguna clave requerida.
        Lanza ValueError si algún dato no cumple las validaciones de negocio.
        """
        for clave in ["codigo", "nombre", "categoria", "precio", "stock"]:
            if clave not in datos:
                raise KeyError(f"Clave faltante '{clave}' en los datos del producto.")

        return cls(
            codigo=str(datos["codigo"]),
            nombre=str(datos["nombre"]),
            categoria=str(datos["categoria"]),
            precio=datos["precio"],
            stock=datos["stock"]
        )

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre} ({self.categoria}) | ${self.precio:.2f} | Stock: {self.stock}"
