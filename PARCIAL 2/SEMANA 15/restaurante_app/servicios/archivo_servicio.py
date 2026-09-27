# -*- coding: utf-8 -*-
"""
Servicio de Persistencia en Archivos JSON - Restaurante App (Semana 15)
======================================================================
Asignatura: Programación Orientada a Objetos (UEA)
Estudiante: Lilibeth Demera

Mantiene la responsabilidad exclusiva de interactuar con el sistema de archivos local.
Maneja de forma robusta la lectura y escritura de productos.json, usuarios.json y ventas.json,
gestionando excepciones como FileNotFoundError, JSONDecodeError, PermissionError y OSError.
"""

import os
import json
from typing import List, Dict, Any, Optional


class ArchivoServicio:
    """
    Servicio encargado de la persistencia de datos en formato JSON.
    Garantiza que ninguna otra capa del sistema acceda directamente al disco.
    """

    def __init__(
        self,
        ruta_productos: str,
        ruta_usuarios: str,
        ruta_ventas: Optional[str] = None
    ) -> None:
        """
        Inicializa el servicio con las rutas resueltas a los archivos de datos.
        
        :param ruta_productos: Ruta al archivo productos.json.
        :param ruta_usuarios: Ruta al archivo usuarios.json.
        :param ruta_ventas: Ruta al archivo ventas.json (opcional, calculada si se omite).
        """
        self.ruta_productos = os.path.abspath(ruta_productos)
        self.ruta_usuarios = os.path.abspath(ruta_usuarios)
        
        if ruta_ventas:
            self.ruta_ventas = os.path.abspath(ruta_ventas)
        else:
            directorio_base = os.path.dirname(self.ruta_productos)
            self.ruta_ventas = os.path.abspath(os.path.join(directorio_base, "ventas.json"))

    # =========================================================================
    # Persistencia de Productos
    # =========================================================================

    def cargar_datos_productos(self) -> List[Dict[str, Any]]:
        """
        Lee el archivo JSON de productos y retorna la lista de diccionarios correspondiente.
        
        :return: Lista de diccionarios con datos de productos.
        :raises FileNotFoundError: Si el archivo no existe.
        :raises json.JSONDecodeError: Si el archivo contiene JSON malformado.
        :raises PermissionError: Si no hay permisos de lectura.
        :raises ValueError: Si la estructura raíz no es una lista.
        """
        if not os.path.exists(self.ruta_productos):
            raise FileNotFoundError(f"El archivo de productos '{self.ruta_productos}' no fue encontrado.")

        try:
            with open(self.ruta_productos, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Error al decodificar JSON en '{self.ruta_productos}': {e.msg}", e.doc, e.pos
            )
        except PermissionError as e:
            raise PermissionError(f"Sin permisos de lectura sobre '{self.ruta_productos}': {e}")

        if not isinstance(datos, list):
            raise ValueError(f"El archivo '{self.ruta_productos}' debe contener una lista de productos.")

        return datos

    def guardar_datos_productos(self, datos: List[Dict[str, Any]]) -> None:
        """
        Escribe la lista de productos serializados en el archivo JSON.
        Crea las carpetas contenedoras si no existen y escribe de forma atómica.
        
        :param datos: Lista de diccionarios representando los productos.
        :raises PermissionError: Si el sistema operativo deniega la escritura.
        :raises OSError: Si ocurre un error de E/S en el disco.
        """
        if not isinstance(datos, list):
            raise ValueError("Los datos a guardar deben ser una lista de diccionarios de productos.")

        directorio = os.path.dirname(self.ruta_productos)
        if not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

        try:
            with open(self.ruta_productos, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
        except PermissionError as e:
            raise PermissionError(f"Sin permisos de escritura en '{self.ruta_productos}': {e}")
        except OSError as e:
            raise OSError(f"Error del sistema al guardar en '{self.ruta_productos}': {e}")

    # =========================================================================
    # Persistencia de Usuarios
    # =========================================================================

    def cargar_datos_usuarios(self) -> List[Dict[str, Any]]:
        """
        Lee el archivo JSON de usuarios y retorna la lista de diccionarios correspondiente.
        
        :return: Lista de diccionarios con datos de usuarios.
        :raises FileNotFoundError: Si el archivo no existe.
        :raises json.JSONDecodeError: Si el archivo contiene JSON malformado.
        :raises PermissionError: Si no hay permisos de lectura.
        :raises ValueError: Si la estructura raíz no es una lista.
        """
        if not os.path.exists(self.ruta_usuarios):
            raise FileNotFoundError(f"El archivo de usuarios '{self.ruta_usuarios}' no fue encontrado.")

        try:
            with open(self.ruta_usuarios, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Error al decodificar JSON en '{self.ruta_usuarios}': {e.msg}", e.doc, e.pos
            )
        except PermissionError as e:
            raise PermissionError(f"Sin permisos de lectura sobre '{self.ruta_usuarios}': {e}")

        if not isinstance(datos, list):
            raise ValueError(f"El archivo '{self.ruta_usuarios}' debe contener una lista de usuarios.")

        return datos

    # =========================================================================
    # Persistencia de Ventas (Semana 15)
    # =========================================================================

    def cargar_datos_ventas(self) -> List[Dict[str, Any]]:
        """
        Lee el archivo JSON de ventas y retorna la lista de diccionarios correspondiente.
        Si el archivo no existe, lo crea automáticamente inicializado como lista vacía.
        
        :return: Lista de diccionarios con datos de ventas.
        :raises json.JSONDecodeError: Si el archivo contiene JSON malformado.
        :raises PermissionError: Si no hay permisos de lectura.
        :raises ValueError: Si la estructura raíz no es una lista.
        """
        if not os.path.exists(self.ruta_ventas):
            # Crear archivo vacío inicial si no existe
            self.guardar_datos_ventas([])
            return []

        try:
            with open(self.ruta_ventas, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Error al decodificar JSON en '{self.ruta_ventas}': {e.msg}", e.doc, e.pos
            )
        except PermissionError as e:
            raise PermissionError(f"Sin permisos de lectura sobre '{self.ruta_ventas}': {e}")

        if not isinstance(datos, list):
            raise ValueError(f"El archivo '{self.ruta_ventas}' debe contener una lista de ventas.")

        return datos

    def guardar_datos_ventas(self, datos: List[Dict[str, Any]]) -> None:
        """
        Escribe la lista de ventas serializadas en el archivo JSON.
        Crea las carpetas contenedoras si no existen y escribe con codificación UTF-8.
        
        :param datos: Lista de diccionarios representando las ventas.
        :raises PermissionError: Si el sistema operativo deniega la escritura.
        :raises OSError: Si ocurre un error de E/S en el disco.
        """
        if not isinstance(datos, list):
            raise ValueError("Los datos a guardar deben ser una lista de diccionarios de ventas.")

        directorio = os.path.dirname(self.ruta_ventas)
        if not os.path.exists(directorio):
            os.makedirs(directorio, exist_ok=True)

        try:
            with open(self.ruta_ventas, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
        except PermissionError as e:
            raise PermissionError(f"Sin permisos de escritura en '{self.ruta_ventas}': {e}")
        except OSError as e:
            raise OSError(f"Error del sistema al guardar en '{self.ruta_ventas}': {e}")
