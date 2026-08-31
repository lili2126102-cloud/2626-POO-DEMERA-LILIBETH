# -*- coding: utf-8 -*-
from typing import Optional, Set, List
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta

class Restaurante:
    """
    Clase de servicio encargada de administrar las colecciones del restaurante.
    Gestiona listas internas de productos, usuarios y ventas aplicando encapsulación para
    evitar que el programa principal modifique directamente los datos internos.
    """

    def __init__(self, nombre_establecimiento: str = "El Gran Sabor") -> None:
        """
        Constructor del servicio Restaurante.
        Inicializa listas privadas para productos, usuarios y ventas.
        """
        self.nombre_establecimiento: str = nombre_establecimiento
        self._productos: List[Producto] = []
        self._usuarios: List[Usuario] = []
        self._ventas: List[Venta] = []

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

    @property
    def ventas(self) -> List[Venta]:
        """
        Retorna una copia de la lista de ventas.
        Evita que main.py modifique directamente la lista interna.
        """
        return list(self._ventas)

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

    def actualizar_producto(self, codigo: str, nuevo_nombre: str, nueva_categoria: str, nuevo_precio: float, nuevo_stock: int) -> bool:
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
            producto.stock = nuevo_stock
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

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        """
        Busca un usuario registrado por su número de identificación.
        Retorna el objeto Usuario correspondiente o None si no existe.
        """
        identificacion_limpia = identificacion.strip().lower()
        for u in self._usuarios:
            if u.identificacion.lower() == identificacion_limpia:
                return u
        return None

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

    # === Operaciones de Venta ===

    def vender_producto(self, codigo_producto: str, identificacion_usuario: str, cantidad: int) -> bool:
        """
        Realiza la venta de un producto a un usuario registrado.
        Comprueba que:
        - El usuario exista.
        - El producto exista.
        - La cantidad solicitada sea válida (> 0).
        - Exista suficiente stock disponible.
        
        Si todo es válido, reduce el stock del producto, agrega la venta a la colección
        de ventas y retorna True. En caso contrario, lanza ValueError con la explicación.
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
        self._ventas.append(nueva_venta)

        # Disminuir el stock del producto
        producto.vender(cantidad_num)

        return True

    def consultar_ventas_usuario(self, identificacion_usuario: str) -> List[Venta]:
        """
        Retorna la lista de ventas asociadas a un usuario en particular,
        recorriendo y filtrando la colección de ventas.
        """
        identificacion_limpia = identificacion_usuario.strip().lower()
        ventas_usuario: List[Venta] = []
        
        for venta in self._ventas:
            if venta.usuario_id.lower() == identificacion_limpia:
                ventas_usuario.append(venta)
                
        return ventas_usuario

    # === Operaciones de Carga/Catálogo ===

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

    def actualizar_catalogo_ventas(self, ventas: List[Venta]) -> None:
        """
        Reemplaza la lista actual de ventas por la lista de ventas suministrada.
        """
        self._ventas = ventas
