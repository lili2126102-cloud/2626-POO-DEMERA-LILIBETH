# -*- coding: utf-8 -*-
"""
Servicio de Negocio - Restaurante App (Semana 15)
================================================
Asignatura: Programación Orientada a Objetos (UEA)
Estudiante: Lilibeth Demera

Centraliza las reglas de negocio, las validaciones de dominio y las operaciones
sobre los modelos Producto, Usuario y Venta.
Garantiza que la interfaz gráfica (UI) no manipule datos ni archivos JSON directamente,
coordinando el flujo: UI -> command= -> Callback -> Servicio -> Persistencia -> Respuesta.
"""

from datetime import datetime
from typing import List, Optional, Set
import re

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    """
    Servicio principal del dominio del restaurante.
    Gestiona las colecciones en memoria y delega la persistencia en ArchivoServicio.
    """

    def __init__(self, archivo_servicio: ArchivoServicio) -> None:
        """
        Inicializa el servicio inyectando la persistencia.
        
        :param archivo_servicio: Instancia de ArchivoServicio.
        """
        self.archivo_servicio = archivo_servicio
        self._productos: List[Producto] = []
        self._usuarios: List[Usuario] = []
        self._ventas: List[Venta] = []

    # =========================================================================
    # Propiedades de acceso a colecciones
    # =========================================================================

    @property
    def productos(self) -> List[Producto]:
        """Retorna una copia superficial de la lista de productos."""
        return list(self._productos)

    @property
    def usuarios(self) -> List[Usuario]:
        """Retorna una copia superficial de la lista de usuarios."""
        return list(self._usuarios)

    @property
    def ventas(self) -> List[Venta]:
        """Retorna una copia superficial de la lista de ventas."""
        return list(self._ventas)

    # =========================================================================
    # Carga Inicial y Persistencia
    # =========================================================================

    def cargar_datos(self) -> None:
        """Carga productos, usuarios y ventas desde los archivos persistentes."""
        self._cargar_productos()
        self._cargar_usuarios()
        self._cargar_ventas()

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

    def _cargar_ventas(self) -> None:
        """Carga y valida las ventas desde el archivo JSON (Semana 15)."""
        self._ventas.clear()
        try:
            datos = self.archivo_servicio.cargar_datos_ventas()
            for item in datos:
                try:
                    venta = Venta.from_dict(item)
                    self._ventas.append(venta)
                except (KeyError, ValueError) as e:
                    print(f"[Aviso] Venta omitida por datos inválidos: {e}")
        except Exception as e:
            print(f"[Error] No fue posible cargar las ventas: {e}")

    def _persistir_productos(self) -> None:
        """Sincroniza la lista actual de productos con el archivo JSON de persistencia."""
        datos_dict = [p.to_dict() for p in self._productos]
        self.archivo_servicio.guardar_datos_productos(datos_dict)

    def _persistir_ventas(self) -> None:
        """Sincroniza la lista actual de ventas con el archivo JSON de persistencia."""
        datos_dict = [v.to_dict() for v in self._ventas]
        self.archivo_servicio.guardar_datos_ventas(datos_dict)

    # =========================================================================
    # Operaciones de Acceso / Autenticación
    # =========================================================================

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

    # =========================================================================
    # Operaciones CRUD sobre Productos
    # =========================================================================

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
        """Busca un producto por su código único."""
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
        """Actualiza los datos de un producto existente."""
        producto = self.buscar_producto(codigo)
        if producto is None:
            raise ValueError(f"No se encontró ningún producto con el código '{codigo}'.")

        producto.nombre = nombre
        producto.categoria = categoria
        producto.precio = precio
        producto.stock = stock

        self._persistir_productos()
        return producto

    def eliminar_producto(self, codigo: str) -> Producto:
        """Elimina un producto del catálogo por su código identificador."""
        producto = self.buscar_producto(codigo)
        if producto is None:
            raise ValueError(f"No se puede eliminar: el producto con código '{codigo}' no existe.")

        self._productos.remove(producto)
        self._persistir_productos()
        return producto

    # =========================================================================
    # Operaciones del Módulo de Ventas (Semana 15)
    # =========================================================================

    def generar_siguiente_id_venta(self) -> str:
        """
        Genera el próximo ID secuencial de venta con formato 'VEN-XXX'.
        Analiza las ventas existentes para evitar duplicaciones.
        """
        numeros = []
        for v in self._ventas:
            match = re.search(r'\d+', v.id_venta)
            if match:
                numeros.append(int(match.group()))
        
        siguiente = max(numeros, default=0) + 1
        return f"VEN-{siguiente:03d}"

    def registrar_venta(
        self,
        id_usuario: str,
        codigo_producto: str,
        cantidad: int = 1
    ) -> Venta:
        """
        Registra una nueva venta ejecutando las reglas de negocio del restaurante:
        1. Valida la existencia del usuario.
        2. Valida la existencia del producto.
        3. Valida que la cantidad sea mayor o igual a 1.
        4. Comprueba que haya stock suficiente para satisfacer la orden.
        5. Reduce el inventario disponible del producto vendido.
        6. Persiste la actualización de productos.json.
        7. Crea y registra la transacción en ventas.json.
        
        :param id_usuario: Identificación del usuario registrado.
        :param codigo_producto: Código del producto del catálogo.
        :param cantidad: Unidades vendidas (por defecto 1).
        :return: Instancia de la Venta registrada.
        :raises ValueError: Si alguna regla de negocio no se cumple.
        """
        # 1. Validación de usuario
        if not id_usuario or not str(id_usuario).strip():
            raise ValueError("Debe seleccionar un usuario para registrar la venta.")
        
        usuario = self.buscar_usuario(id_usuario.strip())
        if usuario is None:
            raise ValueError(f"No se encontró ningún usuario con identificación '{id_usuario}'.")

        # 2. Validación de producto
        if not codigo_producto or not str(codigo_producto).strip():
            raise ValueError("Debe seleccionar un producto para registrar la venta.")

        producto = self.buscar_producto(codigo_producto.strip())
        if producto is None:
            raise ValueError(f"No se encontró ningún producto con código '{codigo_producto}'.")

        # 3. Validación de cantidad
        try:
            cant_int = int(cantidad)
        except (ValueError, TypeError):
            raise ValueError("La cantidad debe ser un número entero válido.")

        if cant_int < 1:
            raise ValueError("La cantidad a vender debe ser al menos 1 unidad.")

        # 4. Validación de stock disponible
        if producto.stock < cant_int:
            raise ValueError(
                f"Stock insuficiente para '{producto.nombre}'. "
                f"Disponibles: {producto.stock} unidades | Solicitadas: {cant_int}."
            )

        # 5. Descuento de stock en el producto
        producto.stock -= cant_int
        self._persistir_productos()

        # 6. Generación del identificador y fecha de la venta
        id_venta = self.generar_siguiente_id_venta()
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 7. Creación y persistencia de la Venta
        nueva_venta = Venta(
            id_venta=id_venta,
            id_usuario=usuario.identificacion,
            nombre_usuario=usuario.nombre,
            codigo_producto=producto.codigo,
            nombre_producto=producto.nombre,
            precio_unitario=producto.precio,
            cantidad=cant_int,
            fecha=fecha_actual
        )

        self._ventas.append(nueva_venta)
        self._persistir_ventas()
        return nueva_venta

    def buscar_venta(self, id_venta: str) -> Optional[Venta]:
        """Busca una venta por su identificador único."""
        if not id_venta:
            return None
        id_buscado = id_venta.strip().upper()
        for v in self._ventas:
            if v.id_venta.upper() == id_buscado:
                return v
        return None

    def obtener_ventas_por_usuario(self, identificacion: str) -> List[Venta]:
        """Retorna las ventas asociadas a un usuario específico."""
        id_buscado = identificacion.strip().lower()
        return [v for v in self._ventas if v.id_usuario.strip().lower() == id_buscado]

    # =========================================================================
    # Consultas y Métricas
    # =========================================================================

    def listar_productos(self) -> List[Producto]:
        """Retorna una lista independiente con todos los productos registrados."""
        return list(self._productos)

    def listar_usuarios(self) -> List[Usuario]:
        """Retorna una lista independiente con todos los usuarios registrados."""
        return list(self._usuarios)

    def listar_ventas(self) -> List[Venta]:
        """Retorna la lista de ventas registradas (ordenadas por fecha descendente)."""
        return sorted(self._ventas, key=lambda v: v.fecha, reverse=True)

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

    def obtener_cantidad_ventas(self) -> int:
        """Retorna el número total de ventas registradas."""
        return len(self._ventas)

    def obtener_total_ingresos_ventas(self) -> float:
        """Calcula los ingresos monetarios totales acumulados por todas las ventas."""
        return sum(v.total for v in self._ventas)

    def obtener_total_unidades_vendidas(self) -> int:
        """Calcula el total de unidades de productos despachadas en ventas."""
        return sum(v.cantidad for v in self._ventas)

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
