# -*- coding: utf-8 -*-
"""
Paquete de Modelos del Dominio — Semana 15
=========================================
Exporta las clases fundamentales que representan las entidades del restaurante:
Producto, Usuario y Venta.
"""

from .producto import Producto
from .usuario import Usuario
from .venta import Venta

__all__ = ["Producto", "Usuario", "Venta"]
