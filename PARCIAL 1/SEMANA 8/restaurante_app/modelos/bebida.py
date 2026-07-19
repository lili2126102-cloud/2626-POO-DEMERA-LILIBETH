# -*- coding: utf-8 -*-
from modelos.producto import Producto

class Bebida(Producto):
    """
    Clase que representa una bebida en el restaurante.
    Hereda de la clase base Producto (LSP) e incorpora atributos específicos
    como tamaño y tipo de envase.
    """

    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float, tamano: str, tipo_envase: str) -> None:
        """
        Constructor de la clase Bebida.
        Delega la inicialización de los atributos comunes a la clase Producto
        e inicializa los específicos de Bebida a través de sus setters.
        """
        super().__init__(codigo, nombre, categoria, precio)
        self.tamano = tamano
        self.tipo_envase = tipo_envase

    # --- Propiedad: tamano ---
    @property
    def tamano(self) -> str:
        """Getter para obtener el tamaño de la bebida."""
        return self._tamano

    @tamano.setter
    def tamano(self, valor: str) -> None:
        """Setter para validar y asignar el tamaño de la bebida."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El tamaño de la bebida no puede estar vacío.")
        self._tamano = valor.strip()

    # --- Propiedad: tipo_envase ---
    @property
    def tipo_envase(self) -> str:
        """Getter para obtener el tipo de envase de la bebida."""
        return self._tipo_envase

    @tipo_envase.setter
    def tipo_envase(self, valor: str) -> None:
        """Setter para validar y asignar el tipo de envase de la bebida."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El tipo de envase de la bebida no puede estar vacío.")
        self._tipo_envase = valor.strip()

    def mostrar_informacion(self) -> None:
        """
        Muestra la información completa de la bebida, reutilizando el método
        de la clase base Producto y agregando los detalles específicos de la bebida.
        """
        super().mostrar_informacion()
        print(f"Tamaño: {self.tamano}")
        print(f"Tipo de Envase: {self.tipo_envase}")
