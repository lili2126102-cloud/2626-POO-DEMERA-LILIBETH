# -*- coding: utf-8 -*-

class Usuario:
    """
    Clase que representa un usuario registrado en el sistema del restaurante.
    Se utiliza tanto para la simulación de autenticación (login)
    como para la consulta de usuarios en la interfaz principal.
    """

    def __init__(self, identificacion: str, nombre: str, correo: str, clave: str = "1234") -> None:
        """
        Constructor de la clase Usuario.
        Inicializa los atributos utilizando sus setters para aplicar las validaciones correspondientes.
        """
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo
        self.clave = clave

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

    # --- Propiedad: clave ---
    @property
    def clave(self) -> str:
        """Getter para obtener la clave de acceso del usuario."""
        return self._clave

    @clave.setter
    def clave(self, valor: str) -> None:
        """Setter para validar y asignar la contraseña del usuario."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La contraseña del usuario no puede estar vacía.")
        self._clave = valor.strip()

    def validar_credencial(self, clave_ingresada: str) -> bool:
        """
        Comprueba si la contraseña ingresada coincide con la del usuario.
        """
        return self._clave == clave_ingresada.strip()

    def to_dict(self) -> dict:
        """
        Convierte el objeto Usuario en un diccionario para serialización JSON.
        """
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "clave": self.clave
        }

    @classmethod
    def from_dict(cls, datos: dict) -> 'Usuario':
        """
        Reconstruye un objeto Usuario a partir de un diccionario de datos.
        Lanza KeyError si falta alguna de las claves requeridas.
        Lanza ValueError si los datos no pasan las validaciones de la clase.
        """
        for clave_req in ["identificacion", "nombre", "correo"]:
            if clave_req not in datos:
                raise KeyError(f"Clave faltante '{clave_req}' en los datos del usuario.")

        # Si el JSON no incluye 'clave', se asigna '1234' por defecto
        clave_acceso = str(datos.get("clave", "1234"))

        return cls(
            identificacion=str(datos["identificacion"]),
            nombre=str(datos["nombre"]),
            correo=str(datos["correo"]),
            clave=clave_acceso
        )

    def __str__(self) -> str:
        return f"{self.identificacion} - {self.nombre} ({self.correo})"
