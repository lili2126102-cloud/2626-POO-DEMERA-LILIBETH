# -*- coding: utf-8 -*-
"""
Servicio de Negocio - Restaurante App (Semana 14)
================================================
Centraliza las reglas de negocio, las validaciones de dominio y las operaciones
sobre los modelos Producto y Usuario. Garantiza que la interfaz gráfica (UI)
no manipule datos ni archivos JSON directamente.
"""

from typing import List, Optional, Set
from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    """
    Servicio principal del dominio del restaurante.
    Gestiona colecciones en memoria y delega la persistencia a ArchivoServicio.
    """

    def __init__(self, archivo_servicio: ArchivoServicio) -> None:
        """
        Inicializa el servicio inyectando la persistencia.
        
        :param archivo_servicio: Instancia de ArchivoServicio.
        """
        self.archivo_servicio = archivo_servicio
        self._productos: List[Producto] = []
        self._usuarios: List[Usuario] = []

    @property
    def productos(self) -> List[Producto]:
        """Retorna una copia superficial de la lista de productos."""
        return list(self._productos)

    @property
    def usuarios(self) -> List[Usuario]:
        """Retorna una copia superficial de la lista de usuarios."""
        return list(self._usuarios)

    # === Carga Inicial de Datos ===

    def cargar_datos(self) -> None:
        """Carga los productos y usuarios desde los archivos persistentes."""
        self._cargar_productos()
        self._cargar_usuarios()

    def _cargar_productos(self) -> None:
        """Carga y valida los productos desde el archivo JSON."""
        self._productos.clear()
        try:
            datos = self.archivo_servicio.cargar_datos_productos()
            for item in datos:
                try:
                    producto = Producto.from_dict(item)
                    self._productos.append(producto)
                except (KeyError, ValueError) as e:
                    print(f"[Aviso] Producto omitido por datos inválidos: {e}")
        except Exception as e:
            print(f"[Error] No fue posible cargar los productos: {e}")

    def _cargar_usuarios(self) -> None:
        """Carga y valida los usuarios desde el archivo JSON."""
        self._usuarios.clear()
        try:
            datos = self.archivo_servicio.cargar_datos_usuarios()
            for item in datos:
                try:
                    usuario = Usuario.from_dict(item)
                    self._usuarios.append(usuario)
                except (KeyError, ValueError) as e:
                    print(f"[Aviso] Usuario omitido por datos inválidos: {e}")
        except Exception as e:
            print(f"[Error] No fue posible cargar los usuarios: {e}")

    def _persistir_productos(self) -> None:
        """Sincroniza la lista actual de productos con el archivo JSON de persistencia."""
        datos_dict = [p.to_dict() for p in self._productos]
        self.archivo_servicio.guardar_datos_productos(datos_dict)

    # === Operaciones de Acceso / Autenticación ===

    def validar_acceso(self, identificador: str, clave: str) -> Optional[Usuario]:
        """
        Valida las credenciales ingresadas.
        Permite el acceso mediante identificación o correo electrónico.
        """
        if not identificador or not clave:
            return None

        id_limpio = identificador.strip().lower()
        clave_limpia = clave.strip()

        for usuario in self._usuarios:
            coincide_identificacion = usuario.identificacion.strip().lower() == id_limpio
            coincide_correo = usuario.correo.strip().lower() == id_limpio

            if (coincide_identificacion or coincide_correo) and usuario.validar_credencial(clave_limpia):
                return usuario

        return None

    # === Operaciones CRUD sobre Productos (Semana 14) ===

    def registrar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int
    ) -> Producto:
        """
        Registra un nuevo producto en el catálogo previa validación de negocio:
        - El código debe ser único en el sistema.
        - Las validaciones de tipos y valores son ejercidas por el modelo Producto.
        Persiste inmediatamente los cambios en productos.json.
        
        :return: El objeto Producto creado.
        :raises ValueError: Si el código ya existe o los valores no son válidos.
        """
        if not codigo or not codigo.strip():
            raise ValueError("El código del producto es obligatorio.")

        codigo_limpio = codigo.strip().upper()
        if self.buscar_producto(codigo_limpio) is not None:
            raise ValueError(f"Ya existe un producto registrado con el código '{codigo_limpio}'.")

        nuevo_producto = Producto(
            codigo=codigo_limpio,
            nombre=nombre,
            categoria=categoria,
            precio=precio,
            stock=stock
        )

        self._productos.append(nuevo_producto)
        self._persistir_productos()
        return nuevo_producto

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        """
        Busca un producto por su código único (búsqueda insensible a mayúsculas/minúsculas).
        
        :param codigo: Código identificador a buscar.
        :return: Producto encontrado o None si no existe.
        """
        if not codigo:
            return None
        codigo_buscado = codigo.strip().upper()
        for p in self._productos:
            if p.codigo.upper() == codigo_buscado:
                return p
        return None

    def actualizar_producto(
        self,
        codigo: str,
        nombre: str,
        categoria: str,
        precio: float,
        stock: int
    ) -> Producto:
        """
        Actualiza los datos de un producto existente.
        
        :param codigo: Código del producto a modificar.
        :param nombre: Nuevo nombre.
        :param categoria: Nueva categoría.
        :param precio: Nuevo precio unitario.
        :param stock: Nuevo stock disponible.
        :return: Producto actualizado.
        :raises ValueError: Si el producto no existe o los valores no son válidos.
        """
        producto = self.buscar_producto(codigo)
        if producto is None:
            raise ValueError(f"No se encontró ningún producto con el código '{codigo}'.")

        # Aplicar modificaciones a través de los setters para disparar validaciones
        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio
        producto.stock = stock

        self._persistir_productos()
        return producto

    def eliminar_producto(self, codigo: str) -> Producto:
        """
        Elimina un producto del catálogo por su código identificador.
        
        :param codigo: Código del producto a eliminar.
        :return: El objeto Producto eliminado.
        :raises ValueError: Si el producto no existe.
        """
        producto = self.buscar_producto(codigo)
        if producto is None:
            raise ValueError(f"No se puede eliminar: el producto con código '{codigo}' no existe.")

        self._productos.remove(producto)
        self._persistir_productos()
        return producto

    # === Consultas y Métricas de Información ===

    def listar_productos(self) -> List[Producto]:
        """Retorna una lista independiente con todos los productos registrados."""
        return list(self._productos)

    def listar_usuarios(self) -> List[Usuario]:
        """Retorna una lista independiente con todos los usuarios registrados."""
        return list(self._usuarios)

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        """Busca un usuario por su cédula o identificación."""
        id_buscado = identificacion.strip().lower()
        for u in self._usuarios:
            if u.identificacion.strip().lower() == id_buscado:
                return u
        return None

    def obtener_cantidad_productos(self) -> int:
        """Retorna el número total de productos disponibles."""
        return len(self._productos)

    def obtener_cantidad_usuarios(self) -> int:
        """Retorna el número total de usuarios registrados."""
        return len(self._usuarios)

    def obtener_total_stock(self) -> int:
        """Calcula la sumatoria del stock acumulado de todos los productos."""
        return sum(p.stock for p in self._productos)

    def obtener_categorias_unicas(self) -> List[str]:
        """
        Retorna la lista ordenada de categorías únicas existentes en el catálogo
        más las categorías estándar del restaurante.
        """
        categorias: Set[str] = {
            "Carnes", "Mariscos", "Bebidas", "Postres", "Entradas", "Pastas", "Ensaladas"
        }
        for p in self._productos:
            if p.categoria:
                categorias.add(p.categoria)
        return sorted(list(categorias))
