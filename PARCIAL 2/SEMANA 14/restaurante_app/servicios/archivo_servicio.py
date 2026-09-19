# -*- coding: utf-8 -*-
"""
Servicio de Persistencia en Archivos JSON - Restaurante App (Semana 14)
======================================================================
Mantiene la responsabilidad exclusiva de interactuar con el sistema de archivos local.
Maneja de forma robusta la lectura y escritura de productos.json y usuarios.json,
gestionando excepciones como FileNotFoundError, JSONDecodeError, PermissionError y OSError.
"""

import os
import json
from typing import List, Dict, Any


class ArchivoServicio:
    """
    Servicio encargado de la persistencia de datos en formato JSON.
    Garantiza que ninguna otra capa del sistema acceda directamente al disco.
    """

    def __init__(self, ruta_productos: str, ruta_usuarios: str) -> None:
        """
        Inicializa el servicio con las rutas resueltas a los archivos de datos.
        
        :param ruta_productos: Ruta al archivo productos.json.
        :param ruta_usuarios: Ruta al archivo usuarios.json.
        """
        self.ruta_productos = os.path.abspath(ruta_productos)
        self.ruta_usuarios = os.path.abspath(ruta_usuarios)

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
