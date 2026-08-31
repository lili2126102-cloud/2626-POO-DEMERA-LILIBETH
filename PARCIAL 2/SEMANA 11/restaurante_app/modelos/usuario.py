# -*- coding: utf-8 -*-

class Usuario:
    """
    Clase que representa un usuario registrado en el sistema del restaurante.
    Representa de forma general a las personas registradas, permitiendo
    que el proyecto pueda evolucionar posteriormente hacia diferentes tipos de usuarios.
    """

    def __init__(self, identificacion: str, nombre: str, correo: str) -> None:
        """
        Constructor de la clase Usuario.
        Inicializa los atributos utilizando sus setters para aplicar las validaciones correspondientes.
        """
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo

    # --- Propiedad: identificacion ---
    @property
    def identificacion(self) -> str:
        """Getter para obtener la identificación del usuario."""
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor: str) -> None:
        """Setter para validar y asignar la identificación del usuario."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        self._identificacion = valor.strip()

    # --- Propiedad: nombre ---
    @property
    def nombre(self) -> str:
        """Getter para obtener el nombre del usuario."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Setter para validar y asignar el nombre del usuario."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        self._nombre = valor.strip()

    # --- Propiedad: correo ---
    @property
    def correo(self) -> str:
        """Getter para obtener el correo del usuario."""
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Setter para validar y asignar el correo del usuario."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El correo del usuario no puede estar vacío.")
        valor_limpio = valor.strip()
        if "@" not in valor_limpio or len(valor_limpio) < 3:
            raise ValueError("El correo del usuario debe ser una dirección válida (contener '@').")
        self._correo = valor_limpio

    def mostrar_informacion(self) -> None:
        """
        Muestra en consola la información del usuario.
        """
        print(f"Identificación: {self.identificacion}")
        print(f"Nombre: {self.nombre}")
        print(f"Correo: {self.correo}")

    def to_dict(self) -> dict:
        """
        Convierte el objeto Usuario en un diccionario para serialización JSON.
        """
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo
        }

    @classmethod
    def from_dict(cls, datos: dict) -> 'Usuario':
        """
        Reconstruye un objeto Usuario a partir de un diccionario de datos.
        Lanza KeyError si falta alguna de las claves esperadas.
        Lanza ValueError si los datos no pasan las validaciones de la clase.
        """
        for clave in ["identificacion", "nombre", "correo"]:
            if clave not in datos:
                raise KeyError(f"Clave faltante '{clave}' en los datos del usuario.")
        
        return cls(
            identificacion=datos["identificacion"],
            nombre=datos["nombre"],
            correo=datos["correo"]
        )
