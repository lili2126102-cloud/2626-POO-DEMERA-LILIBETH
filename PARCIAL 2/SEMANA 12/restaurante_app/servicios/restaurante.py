# -*- coding: utf-8 -*-
from typing import Optional, Set, List, Dict
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class Restaurante:
    """
    Clase de servicio encargada de administrar la lógica de negocio y las colecciones
    del restaurante.
    
    En esta versión (Semana 12), se combinan:
    1. Colecciones principales (List): Mantienen el orden secuencial de inserción,
       facilitan el recorrido completo para reportes y son la base para la serialización JSON.
    2. Estructuras auxiliares (Dict y Set): Optimizan las búsquedas, consultas agrupadas
       y validaciones de unicidad a complejidad O(1), manteniéndose permanentemente
       sincronizadas ante cualquier mutación en los datos.
    """

    def __init__(self, nombre_establecimiento: str = "El Gran Sabor") -> None:
        """
        Constructor del servicio Restaurante.
        Inicializa las colecciones principales (listas) y las estructuras de indexación
        auxiliar en memoria (diccionarios y conjuntos).
        """
        self.nombre_establecimiento: str = nombre_establecimiento
        
        # --- Colecciones Principales (List) ---
        # Preservan orden de registro, listado y persistencia a disco.
        self._productos: List[Producto] = []
        self._usuarios: List[Usuario] = []
        self._ventas: List[Venta] = []

        # --- Estructuras de Indexación Auxiliares en Memoria (Dict) ---
        # Permiten búsquedas y validaciones de existencia en tiempo constante O(1).
        self._productos_por_codigo: Dict[str, Producto] = {}
        self._usuarios_por_identificacion: Dict[str, Usuario] = {}
        self._ventas_por_usuario: Dict[str, List[Venta]] = {}

    @property
    def productos(self) -> List[Producto]:
        """
        Retorna una copia superficial de la lista principal de productos.
        Garantiza encapsulación para que agentes externos no alteren la colección interna.
        """
        return list(self._productos)

    @property
    def usuarios(self) -> List[Usuario]:
        """
        Retorna una copia superficial de la lista principal de usuarios.
        Garantiza encapsulación protegiendo la colección interna.
        """
        return list(self._usuarios)

    @property
    def ventas(self) -> List[Venta]:
        """
        Retorna una copia superficial de la lista principal de ventas.
        Garantiza encapsulación protegiendo la colección interna.
        """
        return list(self._ventas)

    # === Operaciones de Producto (CRUD Optimizado con Dict) ===

    def registrar_producto(self, producto: Producto) -> None:
        """
        Registra un nuevo objeto Producto en el sistema.
        
        Optimización O(1): Valida la unicidad del código consultando el diccionario
        auxiliar self._productos_por_codigo en vez de iterar toda la lista O(N).
        
        Sincronización: Al registrar, añade el producto tanto a la lista principal
        como al diccionario de índices.
        """
        clave = producto.codigo.strip().lower()
        if clave in self._productos_por_codigo:
            raise ValueError(f"Ya existe un producto registrado con el código '{producto.codigo}'.")
        
        # Sincronización en ambas colecciones
        self._productos.append(producto)
        self._productos_por_codigo[clave] = producto

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        """
        Busca un producto a partir de su código único.
        
        Optimización O(1): Realiza una búsqueda directa por tabla hash en el diccionario
        auxiliar en lugar de recorrer secuencialmente la lista O(N).
        """
        clave = codigo.strip().lower()
        return self._productos_por_codigo.get(clave)

    def actualizar_producto(self, codigo: str, nuevo_nombre: str, nueva_categoria: str, nuevo_precio: float, nuevo_stock: int) -> bool:
        """
        Actualiza los datos de un producto existente.
        
        Optimización O(1): Localiza el producto inmediatamente con el diccionario auxiliar.
        Sincronización: Al tratarse del mismo objeto en memoria, la actualización de sus
        atributos se refleja inmediatamente tanto en la lista como en el diccionario.
        """
        producto = self.buscar_producto(codigo)
        if producto:
            producto.nombre = nuevo_nombre
            producto.categoria = nueva_categoria
            producto.precio = nuevo_precio
            producto.stock = nuevo_stock
            return True
        return False

    def eliminar_producto(self, codigo: str) -> bool:
        """
        Elimina un producto del catálogo por su código.
        
        Optimización O(1) en verificación: Comprueba de inmediato si existe en el índice.
        Sincronización: Elimina el elemento de la estructura auxiliar (dict.pop) y de la
        lista principal (list.remove), manteniendo consistencia total en memoria.
        """
        clave = codigo.strip().lower()
        if clave in self._productos_por_codigo:
            producto = self._productos_por_codigo.pop(clave)
            self._productos.remove(producto)
            return True
        return False

    def listar_productos(self) -> None:
        """
        Muestra en consola la lista completa de productos.
        Aprovecha la lista principal para conservar el orden secuencial de registro.
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

    # === Operaciones de Usuario (CRUD Optimizado con Dict) ===

    def registrar_usuario(self, usuario: Usuario) -> None:
        """
        Registra un objeto Usuario en el sistema.
        
        Optimización O(1): Valida duplicidad de identificación mediante consulta directa
        en el índice self._usuarios_por_identificacion en O(1), sustituyendo el recorrido O(N).
        
        Sincronización: Agrega el usuario a la lista principal y actualiza el índice auxiliar.
        """
        clave = usuario.identificacion.strip().lower()
        if clave in self._usuarios_por_identificacion:
            raise ValueError(f"Ya existe un usuario registrado con la identificación '{usuario.identificacion}'.")
        
        self._usuarios.append(usuario)
        self._usuarios_por_identificacion[clave] = usuario

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        """
        Busca un usuario por su número de identificación.
        
        Optimización O(1): Acceso hash directo en self._usuarios_por_identificacion
        sin iterar la lista de usuarios.
        """
        clave = identificacion.strip().lower()
        return self._usuarios_por_identificacion.get(clave)

    def listar_usuarios(self) -> None:
        """
        Muestra en consola la lista completa de usuarios registrados.
        Utiliza la lista principal para respetar el orden de almacenamiento.
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

    # === Operaciones de Venta (Optimizado con Dict de Agrupación) ===

    def vender_producto(self, codigo_producto: str, identificacion_usuario: str, cantidad: int) -> bool:
        """
        Realiza la venta de un producto a un usuario registrado.
        
        Optimización O(1):
        - Localización del usuario en O(1) con self.buscar_usuario().
        - Localización del producto en O(1) con self.buscar_producto().
        
        Sincronización: Al concretarse la venta, se agrega a la lista global self._ventas
        y al índice agrupado self._ventas_por_usuario[usuario_id], garantizando que
        futuras consultas no tengan que iterar todo el historial de ventas.
        """
        usuario = self.buscar_usuario(identificacion_usuario)
        if usuario is None:
            raise ValueError(f"El usuario con identificación '{identificacion_usuario}' no existe.")

        producto = self.buscar_producto(codigo_producto)
        if producto is None:
            raise ValueError(f"El producto con código '{codigo_producto}' no existe.")

        try:
            cantidad_num = int(cantidad)
        except (ValueError, TypeError):
            raise ValueError("La cantidad a vender debe ser un número entero válido.")

        if cantidad_num <= 0:
            raise ValueError("La cantidad solicitada debe ser estrictamente mayor que cero.")

        if producto.stock < cantidad_num:
            raise ValueError(f"Stock insuficiente para el producto '{producto.nombre}'. Stock disponible: {producto.stock}, solicitado: {cantidad_num}.")

        # Crear y agregar la venta
        nueva_venta = Venta(
            usuario_id=usuario.identificacion,
            producto_codigo=producto.codigo,
            cantidad=cantidad_num
        )
        
        # Sincronización en colección principal
        self._ventas.append(nueva_venta)

        # Sincronización en índice auxiliar agrupado por usuario
        clave_usuario = usuario.identificacion.strip().lower()
        if clave_usuario not in self._ventas_por_usuario:
            self._ventas_por_usuario[clave_usuario] = []
        self._ventas_por_usuario[clave_usuario].append(nueva_venta)

        # Disminuir el stock del producto
        producto.vender(cantidad_num)

        return True

    def consultar_ventas_usuario(self, identificacion_usuario: str) -> List[Venta]:
        """
        Retorna la lista de ventas asociadas a un usuario en particular.
        
        Optimización O(1): En lugar de recorrer la lista de todas las ventas del restaurante O(V),
        recupera directamente el subconjunto de ventas desde el diccionario auxiliar
        self._ventas_por_usuario usando la identificación como clave.
        """
        clave_usuario = identificacion_usuario.strip().lower()
        ventas_usuario = self._ventas_por_usuario.get(clave_usuario, [])
        return list(ventas_usuario)

    # === Operaciones con Conjuntos (Set) y Reconstrucción de Índices ===

    def obtener_categorias_unicas(self) -> Set[str]:
        """
        Obtiene y retorna las categorías únicas de los productos registrados.
        
        Uso de SET: Aprovecha las propiedades matemáticas de los conjuntos para
        descartar automáticamente categorías duplicadas y permitir operaciones
        de pertenencia eficientes.
        """
        return {p.categoria for p in self._productos}

    def actualizar_catalogo_productos(self, productos: List[Producto]) -> None:
        """
        Carga la lista de productos y reconstruye en memoria el índice auxiliar de búsqueda.
        Garantiza que tras la lectura del JSON, las búsquedas O(1) queden inmediatamente operativas.
        """
        self._productos = list(productos)
        self._productos_por_codigo = {p.codigo.strip().lower(): p for p in self._productos}

    def actualizar_catalogo_usuarios(self, usuarios: List[Usuario]) -> None:
        """
        Carga la lista de usuarios y reconstruye en memoria el índice auxiliar de identificación.
        Garantiza búsquedas O(1) de usuarios desde el inicio de la ejecución.
        """
        self._usuarios = list(usuarios)
        self._usuarios_por_identificacion = {u.identificacion.strip().lower(): u for u in self._usuarios}

    def actualizar_catalogo_ventas(self, ventas: List[Venta]) -> None:
        """
        Carga la lista de ventas y reconstruye en memoria el índice auxiliar agrupado por usuario.
        Evita recorrer todo el histórico de ventas en cada consulta de cliente.
        """
        self._ventas = list(ventas)
        self._ventas_por_usuario = {}
        for venta in self._ventas:
            clave_u = venta.usuario_id.strip().lower()
            if clave_u not in self._ventas_por_usuario:
                self._ventas_por_usuario[clave_u] = []
            self._ventas_por_usuario[clave_u].append(venta)
