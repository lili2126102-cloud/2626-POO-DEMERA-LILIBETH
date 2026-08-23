# -*- coding: utf-8 -*-
import os
import json
from typing import List
from modelos.producto import Producto
from modelos.usuario import Usuario

class ArchivoServicio:
    """
    Servicio encargado del manejo de persistencia de datos (lectura y escritura)
    en formato JSON para productos y usuarios.
    Implementa un manejo robusto de excepciones para garantizar la estabilidad del sistema.
    """

    def __init__(self, ruta_productos: str, ruta_usuarios: str) -> None:
        """
        Constructor del servicio. Recibe las rutas absolutas donde se almacenarán
        los archivos de persistencia de productos y usuarios.
        """
        self.ruta_productos = ruta_productos
        self.ruta_usuarios = ruta_usuarios

    # === Persistencia de Productos ===

    def guardar_productos(self, productos: List[Producto]) -> None:
        """
        Guarda la lista de objetos Producto en el archivo JSON.
        Crea los directorios necesarios si no existen.
        Lanza PermissionError en caso de no tener privilegios suficientes.
        """
        directorio = os.path.dirname(self.ruta_productos)
        if directorio and not os.path.exists(directorio):
            try:
                os.makedirs(directorio, exist_ok=True)
            except PermissionError as e:
                raise PermissionError(f"Permiso denegado al crear la carpeta de datos: {e}")

        try:
            lista_dict = [p.to_dict() for p in productos]
            with open(self.ruta_productos, 'w', encoding='utf-8') as f:
                json.dump(lista_dict, f, indent=4, ensure_ascii=False)
        except PermissionError as e:
            raise PermissionError(f"No se tienen permisos de escritura sobre el archivo '{self.ruta_productos}': {e}")
        except Exception as e:
            raise IOError(f"Error inesperado de E/S al escribir productos: {e}")

    def cargar_productos(self) -> List[Producto]:
        """
        Carga y reconstruye los objetos Producto almacenados en el archivo JSON.
        Lanza FileNotFoundError si el archivo no existe.
        Lanza JSONDecodeError si el formato no es JSON válido.
        Lanza PermissionError si no hay privilegios de lectura.
        Atrapa internamente KeyError y ValueError para omitir registros corruptos o inválidos.
        """
        if not os.path.exists(self.ruta_productos):
            raise FileNotFoundError(f"El archivo de productos '{self.ruta_productos}' no existe.")

        try:
            with open(self.ruta_productos, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Formato JSON inválido en '{self.ruta_productos}': {e.msg}", e.doc, e.pos)
        except PermissionError as e:
            raise PermissionError(f"No se tienen permisos de lectura sobre el archivo '{self.ruta_productos}': {e}")

        if not isinstance(datos, list):
            raise ValueError("La estructura del archivo JSON de productos debe ser una lista.")

        productos: List[Producto] = []
        for idx, item in enumerate(datos):
            try:
                if not isinstance(item, dict):
                    raise ValueError("Cada elemento del catálogo debe ser un diccionario.")
                # Reconstruimos el producto
                producto = Producto.from_dict(item)
                productos.append(producto)
            except KeyError as e:
                print(f"\n\033[93m[ADVERTENCIA] Producto #{idx+1} omitido en la carga: Clave faltante {e}.\033[0m")
            except ValueError as e:
                print(f"\n\033[93m[ADVERTENCIA] Producto #{idx+1} omitido en la carga: Datos inválidos. {e}.\033[0m")

        return productos

    # === Persistencia de Usuarios ===

    def guardar_usuarios(self, usuarios: List[Usuario]) -> None:
        """
        Guarda la lista de objetos Usuario en el archivo JSON.
        Crea los directorios necesarios si no existen.
        Lanza PermissionError en caso de no tener privilegios suficientes.
        """
        directorio = os.path.dirname(self.ruta_usuarios)
        if directorio and not os.path.exists(directorio):
            try:
                os.makedirs(directorio, exist_ok=True)
            except PermissionError as e:
                raise PermissionError(f"Permiso denegado al crear la carpeta de datos: {e}")

        try:
            lista_dict = [u.to_dict() for u in usuarios]
            with open(self.ruta_usuarios, 'w', encoding='utf-8') as f:
                json.dump(lista_dict, f, indent=4, ensure_ascii=False)
        except PermissionError as e:
            raise PermissionError(f"No se tienen permisos de escritura sobre el archivo '{self.ruta_usuarios}': {e}")
        except Exception as e:
            raise IOError(f"Error inesperado de E/S al escribir usuarios: {e}")

    def cargar_usuarios(self) -> List[Usuario]:
        """
        Carga y reconstruye los objetos Usuario almacenados en el archivo JSON.
        Lanza FileNotFoundError si el archivo no existe.
        Lanza JSONDecodeError si el formato no es JSON válido.
        Lanza PermissionError si no hay privilegios de lectura.
        Atrapa internamente KeyError y ValueError para omitir registros corruptos o inválidos.
        """
        if not os.path.exists(self.ruta_usuarios):
            raise FileNotFoundError(f"El archivo de usuarios '{self.ruta_usuarios}' no existe.")

        try:
            with open(self.ruta_usuarios, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(f"Formato JSON inválido en '{self.ruta_usuarios}': {e.msg}", e.doc, e.pos)
        except PermissionError as e:
            raise PermissionError(f"No se tienen permisos de lectura sobre el archivo '{self.ruta_usuarios}': {e}")

        if not isinstance(datos, list):
            raise ValueError("La estructura del archivo JSON de usuarios debe ser una lista.")

        usuarios: List[Usuario] = []
        for idx, item in enumerate(datos):
            try:
                if not isinstance(item, dict):
                    raise ValueError("Cada elemento de usuarios debe ser un diccionario.")
                # Reconstruimos el usuario
                usuario = Usuario.from_dict(item)
                usuarios.append(usuario)
            except KeyError as e:
                print(f"\n\033[93m[ADVERTENCIA] Usuario #{idx+1} omitido en la carga: Clave faltante {e}.\033[0m")
            except ValueError as e:
                print(f"\n\033[93m[ADVERTENCIA] Usuario #{idx+1} omitido en la carga: Datos inválidos. {e}.\033[0m")

        return usuarios
