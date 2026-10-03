# -*- coding: utf-8 -*-
from dataclasses import dataclass

@dataclass
class Cliente:
    """
    Clase que representa un cliente del restaurante.
    Implementada utilizando el decorador @dataclass de Python para
    reducir el código repetitivo de constructores y representaciones.
    """
    nombre: str
    correo: str
    id_cliente: str
