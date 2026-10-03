# -*- coding: utf-8 -*-
"""
Modelo de Usuario - Restaurante App (Semana 16)
===============================================
Representa administradores, empleados y clientes con validaciones de identificación,
correo, credenciales y rol.
"""


class Usuario:
    """
    Entidad que representa un usuario con acceso al sistema.
    Mantiene atributos privados con getters/setters y método de verificación segura.
    """

    ROLES = ("Administrador", "Empleado", "Cliente")

    def __init__(
        self,
        identificacion: str,
        nombre: str,
        correo: str,
        clave: str,
        rol: str = "Cliente"
    ) -> None:
        """
        Inicializa una instancia de Usuario validando sus atributos.
        """
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo
        self.clave = clave
        self.rol = rol

    # --- Propiedad: identificacion ---
    @property
    def identificacion(self) -> str:
        """Getter para el número de identificación / cédula."""
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor: str) -> None:
        """Setter con validación de identificación no vacía."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La identificación del usuario no puede estar vacía.")
        self._identificacion = valor.strip()

    # --- Propiedad: nombre ---
    @property
    def nombre(self) -> str:
        """Getter para el nombre del usuario."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Setter con validación de nombre no vacío."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del usuario no puede estar vacío.")
        self._nombre = valor.strip()

    # --- Propiedad: correo ---
    @property
    def correo(self) -> str:
        """Getter para el correo electrónico."""
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Setter con validación básica de formato de correo."""
        if not isinstance(valor, str) or "@" not in valor or "." not in valor:
            raise ValueError("El correo electrónico ingresado no tiene un formato válido.")
        self._correo = valor.strip().lower()

    # --- Propiedad: clave ---
    @property
    def clave(self) -> str:
        """Getter para la clave de acceso."""
        return self._clave

    @clave.setter
    def clave(self, valor: str) -> None:
        """Setter con validación de contraseña no vacía."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La clave de acceso no puede estar vacía.")
        self._clave = valor.strip()

    @property
    def rol(self) -> str:
        """Rol funcional del usuario dentro del restaurante."""
        return self._rol

    @rol.setter
    def rol(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise ValueError("El rol del usuario no es válido.")
        roles = {rol.casefold(): rol for rol in self.ROLES}
        rol_normalizado = roles.get(valor.strip().casefold())
        if rol_normalizado is None:
            raise ValueError("El rol debe ser Administrador, Empleado o Cliente.")
        self._rol = rol_normalizado

    def validar_credencial(self, clave_ingresada: str) -> bool:
        """
        Compara la clave ingresada con la almacenada.
        
        :param clave_ingresada: Contraseña proporcionada por el usuario.
        :return: True si coincide exactamente, False en caso contrario.
        """
        if not clave_ingresada:
            return False
        return self._clave == clave_ingresada.strip()

    def to_dict(self) -> dict:
        """Serializa el objeto Usuario en un diccionario JSON."""
        return {
            "identificacion": self.identificacion,
            "nombre": self.nombre,
            "correo": self.correo,
            "clave": self.clave,
            "rol": self.rol
        }

    @classmethod
    def from_dict(cls, datos: dict) -> 'Usuario':
        """Reconstruye un objeto Usuario a partir de un diccionario."""
        for clave in ["identificacion", "nombre", "correo", "clave"]:
            if clave not in datos:
                raise KeyError(f"Clave faltante '{clave}' en los datos del usuario.")

        return cls(
            identificacion=str(datos["identificacion"]),
            nombre=str(datos["nombre"]),
            correo=str(datos["correo"]),
            clave=str(datos["clave"]),
            rol=str(datos.get("rol", "Cliente"))
        )

    def __str__(self) -> str:
        return f"{self.identificacion} - {self.nombre} ({self.correo}, {self.rol})"
