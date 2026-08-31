# -*- coding: utf-8 -*-
from typing import Optional, Set, List
from modelos.producto import Producto
from modelos.usuario import Usuario

class Restaurante:
    """
    Clase de servicio encargada de administrar las colecciones del restaurante.
    Gestiona listas internas de productos y usuarios aplicando encapsulación para
    evitar que el programa principal modifique directamente los datos internos.
    """

    def __init__(self, nombre_establecimiento: str = "El Gran Sabor") -> None:
        """
        Constructor del servicio Restaurante.
        Inicializa listas privadas para productos y usuarios.
        """
        self.nombre_establecimiento: str = nombre_establecimiento
        self._productos: List[Producto] = []
        self._usuarios: List[Usuario] = []

    @property
    def productos(self) -> List[Producto]:
        """
        Retorna una copia de la lista de productos.
        Evita que main.py modifique directamente la lista interna.
        """
        return list(self._productos)

    @property
    def usuarios(self) -> List[Usuario]:
        """
        Retorna una copia de la lista de usuarios.
        Evita que main.py modifique directamente la lista interna.
        """
        return list(self._usuarios)

    # === Operaciones de Producto (CRUD) ===

    def registrar_producto(self, producto: Producto) -> None:
        """
        Registra un objeto Producto en la colección.
        Valida que el código del producto no esté duplicado.
        """
        for p in self._productos:
            if p.codigo.lower() == producto.codigo.lower():
                raise ValueError(f"Ya existe un producto registrado con el código '{producto.codigo}'.")
        self._productos.append(producto)

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        """
        Busca un producto por su código único.
        Retorna la instancia del producto si existe, o None en caso contrario.
        """
        codigo_limpio = codigo.strip().lower()
        for p in self._productos:
            if p.codigo.lower() == codigo_limpio:
                return p
        return None

    def actualizar_producto(self, codigo: str, nuevo_nombre: str, nueva_categoria: str, nuevo_precio: float) -> bool:
        """
        Actualiza los campos de un producto existente.
        Retorna True si el producto fue encontrado y actualizado, o False de lo contrario.
        Las validaciones de negocio individuales se ejecutan a través de los setters.
        """
        producto = self.buscar_producto(codigo)
        if producto:
            # Los setters de Producto lanzarán ValueError si los nuevos valores son inválidos
            producto.nombre = nuevo_nombre
            producto.categoria = nueva_categoria
            producto.precio = nuevo_precio
            return True
        return False

    def eliminar_producto(self, codigo: str) -> bool:
        """
        Elimina un producto del catálogo utilizando su código único.
        Retorna True si fue eliminado, o False si no se encontró.
        """
        producto = self.buscar_producto(codigo)
        if producto:
            self._productos.remove(producto)
            return True
        return False

    def listar_productos(self) -> None:
        """
        Muestra en consola la lista completa de productos.
        """
        if not self._productos:
            print("\n\033[93m[!] No hay productos registrados en el menú actualmente.\033[0m")
            return

        print("\n\033[96m==================================================")
        print(f"        MENÚ DE PRODUCTOS - {self.nombre_establecimiento.upper()}")
        print("==================================================\033[0m")
        for idx, producto in enumerate(self._productos, start=1):
            print(f"\n\033[94mNro {idx:02d}:\033[0m")
            producto.mostrar_informacion()
            print("\033[90m" + "-" * 50 + "\033[0m")
        print("\033[96m==================================================\033[0m")

    # === Operaciones de Usuario ===

    def registrar_usuario(self, usuario: Usuario) -> None:
        """
        Registra un objeto Usuario en la colección.
        Valida que la identificación del usuario no esté duplicada.
        """
        for u in self._usuarios:
            if u.identificacion.lower() == usuario.identificacion.lower():
                raise ValueError(f"Ya existe un usuario registrado con la identificación '{usuario.identificacion}'.")
        self._usuarios.append(usuario)

    def listar_usuarios(self) -> None:
        """
        Muestra en consola la lista completa de usuarios registrados.
        """
        if not self._usuarios:
            print("\n\033[93m[!] No hay usuarios registrados en el sistema actualmente.\033[0m")
            return

        print("\n\033[96m==================================================")
        print("             USUARIOS REGISTRADOS")
        print("==================================================\033[0m")
        for idx, usuario in enumerate(self._usuarios, start=1):
            print(f"\n\033[94mNro {idx:02d}:\033[0m")
            usuario.mostrar_informacion()
            print("\033[90m" + "-" * 50 + "\033[0m")
        print("\033[96m==================================================\033[0m")

    # === Operación usando Conjuntos (Set) ===

    def obtener_categorias_unicas(self) -> Set[str]:
        """
        Obtiene y retorna las categorías únicas de los productos registrados.
        Utiliza un conjunto (set) para garantizar que no existan duplicados.
        """
        categorias = set()
        for p in self._productos:
            categorias.add(p.categoria)
        return categorias

    def actualizar_catalogo_productos(self, productos: List[Producto]) -> None:
        """
        Reemplaza la lista actual de productos por la lista de productos suministrada.
        """
        self._productos = productos

    def actualizar_catalogo_usuarios(self, usuarios: List[Usuario]) -> None:
        """
        Reemplaza la lista actual de usuarios por la lista de usuarios suministrada.
        """
        self._usuarios = usuarios

