# -*- coding: utf-8 -*-
import os
import json
from typing import List, Dict, Any

class ArchivoServicio:
    """
    Servicio encargado de la persistencia de datos (lectura de archivos JSON).
    Mantiene la responsabilidad exclusiva de interactuar con el sistema de archivos
    local, garantizando un manejo robusto de excepciones (FileNotFoundError,
    JSONDecodeError, PermissionError) y retornando los datos estructurados.
    """

    def __init__(self, ruta_productos: str, ruta_usuarios: str) -> None:
        """
        Inicializa el servicio con las rutas a los archivos de persistencia.
        """
        self.ruta_productos = os.path.abspath(ruta_productos)
        self.ruta_usuarios = os.path.abspath(ruta_usuarios)

    def cargar_datos_productos(self) -> List[Dict[str, Any]]:
        """
        Lee el archivo JSON de productos y retorna la lista de diccionarios correspondiente.
        Lanza FileNotFoundError si el archivo no existe.
        Lanza json.JSONDecodeError si el contenido no es un JSON válido.
        Lanza PermissionError si no hay permisos de lectura.
        Lanza ValueError si el contenido raíz no es una lista.
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

    def cargar_datos_usuarios(self) -> List[Dict[str, Any]]:
        """
        Lee el archivo JSON de usuarios y retorna la lista de diccionarios correspondiente.
        Lanza FileNotFoundError si el archivo no existe.
        Lanza json.JSONDecodeError si el contenido no es un JSON válido.
        Lanza PermissionError si no hay permisos de lectura.
        Lanza ValueError si el contenido raíz no es una lista.
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
