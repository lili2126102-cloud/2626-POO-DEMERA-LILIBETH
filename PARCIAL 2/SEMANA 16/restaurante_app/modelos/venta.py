# -*- coding: utf-8 -*-
"""
Modelo de Venta - Restaurante App (Semana 15)
==============================================
Asignatura: Programación Orientada a Objetos (UEA)
Estudiante: Lilibeth Demera

Representa una transacción de venta en el restaurante relacionando un usuario,
un producto, la cantidad vendida, el importe total y la fecha de la operación.
Aplica encapsulación rigurosa mediante propiedades (@property y @setter).
"""

from datetime import datetime
from typing import Dict, Any


class Venta:
    """
    Entidad que modela una venta realizada en el restaurante.
    Garantiza la consistencia e integridad de los datos de la transacción:
    - ID de venta no vacío y normalizado.
    - Usuario identificable (cédula y nombre).
    - Producto identificable (código, nombre y precio unitario).
    - Cantidad entera positiva (>= 1).
    - Total calculado a partir del precio unitario y la cantidad.
    - Fecha y hora válida de la operación.
    """

    def __init__(
        self,
        id_venta: str,
        id_usuario: str,
        nombre_usuario: str,
        codigo_producto: str,
        nombre_producto: str,
        precio_unitario: float,
        cantidad: int,
        fecha: str,
        total: float = 0.0
    ) -> None:
        """
        Inicializa una nueva venta validando sus atributos mediante los setters.
        """
        self.id_venta = id_venta
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.codigo_producto = codigo_producto
        self.nombre_producto = nombre_producto
        self.precio_unitario = precio_unitario
        self.cantidad = cantidad
        self.fecha = fecha
        
        # Si no se especifica total o es 0, se calcula automáticamente
        if total <= 0:
            self._total = round(self._precio_unitario * self._cantidad, 2)
        else:
            self._total = round(float(total), 2)

    # --- Propiedad: id_venta ---
    @property
    def id_venta(self) -> str:
        """Retorna el identificador único de la venta."""
        return self._id_venta

    @id_venta.setter
    def id_venta(self, valor: str) -> None:
        """Valida que el identificador no esté vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El identificador de la venta no puede estar vacío.")
        self._id_venta = valor.strip().upper()

    # --- Propiedad: id_usuario ---
    @property
    def id_usuario(self) -> str:
        """Retorna la identificación o cédula del usuario."""
        return self._id_usuario

    @id_usuario.setter
    def id_usuario(self, valor: str) -> None:
        """Valida que la identificación del usuario no esté vacía."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        self._id_usuario = valor.strip()

    # --- Propiedad: nombre_usuario ---
    @property
    def nombre_usuario(self) -> str:
        """Retorna el nombre del usuario que gestionó o registró la venta."""
        return self._nombre_usuario

    @nombre_usuario.setter
    def nombre_usuario(self, valor: str) -> None:
        """Valida que el nombre del usuario no esté vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        self._nombre_usuario = valor.strip()

    # --- Propiedad: codigo_producto ---
    @property
    def codigo_producto(self) -> str:
        """Retorna el código único del producto vendido."""
        return self._codigo_producto

    @codigo_producto.setter
    def codigo_producto(self, valor: str) -> None:
        """Valida que el código del producto no esté vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        self._codigo_producto = valor.strip().upper()

    # --- Propiedad: nombre_producto ---
    @property
    def nombre_producto(self) -> str:
        """Retorna el nombre del producto vendido."""
        return self._nombre_producto

    @nombre_producto.setter
    def nombre_producto(self, valor: str) -> None:
        """Valida que el nombre del producto no esté vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre_producto = valor.strip()

    # --- Propiedad: precio_unitario ---
    @property
    def precio_unitario(self) -> float:
        """Retorna el precio unitario del producto al momento de la venta."""
        return self._precio_unitario

    @precio_unitario.setter
    def precio_unitario(self, valor: float) -> None:
        """Valida que el precio sea numérico y positivo (> 0)."""
        try:
            num = float(valor)
        except (ValueError, TypeError):
            raise ValueError("El precio unitario debe ser un valor numérico.")
        if num <= 0:
            raise ValueError("El precio unitario debe ser mayor que cero.")
        self._precio_unitario = round(num, 2)

    # --- Propiedad: cantidad ---
    @property
    def cantidad(self) -> int:
        """Retorna la cantidad de unidades vendidas."""
        return self._cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        """Valida que la cantidad sea un entero positivo mayor o igual a 1."""
        try:
            num = int(valor)
        except (ValueError, TypeError):
            raise ValueError("La cantidad debe ser un número entero.")
        if num < 1:
            raise ValueError("La cantidad a vender debe ser al menos 1 unidad.")
        self._cantidad = num

    # --- Propiedad: total ---
    @property
    def total(self) -> float:
        """Retorna el valor total de la venta (precio unitario * cantidad)."""
        return self._total

    # --- Propiedad: fecha ---
    @property
    def fecha(self) -> str:
        """Retorna la fecha y hora de la transacción."""
        return self._fecha

    @fecha.setter
    def fecha(self, valor: str) -> None:
        """Valida que la fecha tenga formato válido o no esté vacía."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La fecha de la venta no puede estar vacía.")
        self._fecha = valor.strip()

    def to_dict(self) -> Dict[str, Any]:
        """Serializa la venta en un diccionario estructurado para JSON."""
        return {
            "id_venta": self.id_venta,
            "id_usuario": self.id_usuario,
            "nombre_usuario": self.nombre_usuario,
            "codigo_producto": self.codigo_producto,
            "nombre_producto": self.nombre_producto,
            "precio_unitario": self.precio_unitario,
            "cantidad": self.cantidad,
            "total": self.total,
            "fecha": self.fecha
        }

    @classmethod
    def from_dict(cls, datos: Dict[str, Any]) -> 'Venta':
        """
        Reconstruye un objeto Venta a partir de un diccionario.
        Lanza KeyError si falta alguna clave obligatoria.
        Lanza ValueError si algún dato es inconsistente.
        """
        claves_requeridas = [
            "id_venta", "id_usuario", "nombre_usuario",
            "codigo_producto", "nombre_producto",
            "precio_unitario", "cantidad", "fecha"
        ]
        for c in claves_requeridas:
            if c not in datos:
                raise KeyError(f"Clave faltante '{c}' en los datos de la venta.")

        return cls(
            id_venta=str(datos["id_venta"]),
            id_usuario=str(datos["id_usuario"]),
            nombre_usuario=str(datos["nombre_usuario"]),
            codigo_producto=str(datos["codigo_producto"]),
            nombre_producto=str(datos["nombre_producto"]),
            precio_unitario=float(datos["precio_unitario"]),
            cantidad=int(datos["cantidad"]),
            fecha=str(datos["fecha"]),
            total=float(datos.get("total", 0.0))
        )

    def __str__(self) -> str:
        return (
            f"Venta [{self.id_venta}] - {self.fecha} | "
            f"Usuario: {self.nombre_usuario} | "
            f"Producto: {self.nombre_producto} x{self.cantidad} = ${self.total:.2f}"
        )
