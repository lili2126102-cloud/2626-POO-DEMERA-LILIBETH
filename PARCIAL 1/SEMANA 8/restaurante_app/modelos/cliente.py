# -*- coding: utf-8 -*-

class Cliente:
    """
    Clase que representa un cliente registrado en el restaurante.
    Aplica encapsulación mediante propiedades (@property y @setter) para
    controlar la lectura y modificación de los atributos con validaciones.
    """

    def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
        """
        Constructor de la clase Cliente.
        Inicializa los atributos utilizando sus setters para aplicar las validaciones correspondientes.
        """
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo

    # --- Propiedad: identificacion ---
    @property
    def identificacion(self) -> str:
        """Getter para obtener la identificación del cliente."""
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor: str) -> None:
        """Setter para validar y asignar la identificación del cliente."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La identificación del cliente no puede estar vacía.")
        self._identificacion = valor.strip()

    # --- Propiedad: nombre ---
    @property
    def nombre(self) -> str:
        """Getter para obtener el nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Setter para validar y asignar el nombre del cliente."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")
        self._nombre = valor.strip()

    # --- Propiedad: correo ---
    @property
    def correo(self) -> str:
        """Getter para obtener el correo del cliente."""
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Setter para validar y asignar el correo del cliente."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El correo del cliente no puede vacío.")
        valor_limpio = valor.strip()
        if "@" not in valor_limpio or len(valor_limpio) < 3:
            raise ValueError("El correo del cliente debe ser una dirección de correo válida (contener '@').")
        self._correo = valor_limpio

    def mostrar_informacion(self) -> None:
        """
        Muestra en consola la información del cliente.
        """
        print(f"Identificación: {self.identificacion}")
        print(f"Nombre: {self.nombre}")
        print(f"Correo: {self.correo}")
