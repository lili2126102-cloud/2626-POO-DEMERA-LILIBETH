"""
Módulo que define la clase Restaurante para gestionar los servicios principales
del restaurante como productos, clientes y pedidos.
"""

from modelos.producto import Producto
from modelos.cliente import Cliente


class Restaurante:
    """
    Clase que gestiona las operaciones principales del restaurante.

    Atributos:
        nombre (str): Nombre del restaurante
        direccion (str): Dirección del restaurante
        productos (list): Lista de productos disponibles
        clientes (list): Lista de clientes registrados
        pedidos (list): Lista de pedidos realizados
        contador_pedidos (int): Contador para generar IDs de pedidos
    """

    def __init__(self, nombre, direccion):
        """
        Inicializa una instancia de Restaurante.

        Args:
            nombre (str): Nombre del restaurante
            direccion (str): Dirección del restaurante
        """
        self.nombre = nombre
        self.direccion = direccion
        self.productos = []
        self.clientes = []
        self.pedidos = []
        self.contador_pedidos = 0

    def __str__(self):
        """Retorna una representación en texto del restaurante."""
        return f"Restaurante '{self.nombre}' en {self.direccion} | Productos: {len(self.productos)} | Clientes: {len(self.clientes)}"

    # ========== MÉTODOS DE PRODUCTOS ==========

    def agregar_producto(self, id, nombre, descripcion, precio, categoria):
        """
        Crea y agrega un nuevo producto al restaurante.

        Args:
            id (int): Identificador del producto
            nombre (str): Nombre del producto
            descripcion (str): Descripción del producto
            precio (float): Precio del producto
            categoria (str): Categoría del producto
        """
        # Verificar que el ID no exista
        if any(p.get_id() == id for p in self.productos):
            print(f"Error: Ya existe un producto con ID {id}")
            return

        producto = Producto(id, nombre, descripcion, precio, categoria)
        self.productos.append(producto)
        print(f"✓ Producto '{nombre}' agregado exitosamente")

    def obtener_producto_por_id(self, id):
        """
        Busca un producto por su ID.

        Args:
            id (int): ID del producto a buscar

        Returns:
            Producto: El producto encontrado o None
        """
        for producto in self.productos:
            if producto.get_id() == id:
                return producto
        return None

    def listar_productos(self):
        """Muestra todos los productos disponibles en el restaurante."""
        if not self.productos:
            print("\n⚠ No hay productos registrados")
            return

        print(f"\n{'='*50}")
        print(f"MENÚ DEL RESTAURANTE")
        print(f"{'='*50}")
        for producto in self.productos:
            estado = "✓" if producto.is_disponible() else "✗"
            print(f"{estado} [{producto.get_id()}] {producto.get_nombre():<20} ${producto.get_precio():>7.2f} ({producto.get_categoria()})")
        print(f"{'='*50}")

    def listar_productos_por_categoria(self, categoria):
        """
        Lista los productos de una categoría específica.

        Args:
            categoria (str): Categoría de productos a listar
        """
        productos_categoria = [p for p in self.productos if p.get_categoria().lower() == categoria.lower()]

        if not productos_categoria:
            print(f"\n⚠ No hay productos en la categoría '{categoria}'")
            return

        print(f"\n{'='*50}")
        print(f"PRODUCTOS - CATEGORÍA: {categoria.upper()}")
        print(f"{'='*50}")
        for producto in productos_categoria:
            print(f"[{producto.get_id()}] {producto.get_nombre():<20} ${producto.get_precio():>7.2f}")
        print(f"{'='*50}")

    # ========== MÉTODOS DE CLIENTES ==========

    def registrar_cliente(self, nombre, email, telefono):
        """
        Registra un nuevo cliente en el restaurante.

        Args:
            nombre (str): Nombre del cliente
            email (str): Email del cliente
            telefono (str): Teléfono del cliente
        """
        cliente = Cliente(nombre, email, telefono)
        self.clientes.append(cliente)
        print(f"✓ Cliente '{nombre}' registrado exitosamente con ID {cliente.get_id()}")
        return cliente

    def obtener_cliente_por_id(self, id):
        """
        Busca un cliente por su ID.

        Args:
            id (int): ID del cliente a buscar

        Returns:
            Cliente: El cliente encontrado o None
        """
        for cliente in self.clientes:
            if cliente.get_id() == id:
                return cliente
        return None

    def listar_clientes(self):
        """Muestra todos los clientes registrados."""
        if not self.clientes:
            print("\n⚠ No hay clientes registrados")
            return

        print(f"\n{'='*50}")
        print(f"CLIENTES REGISTRADOS")
        print(f"{'='*50}")
        for cliente in self.clientes:
            print(f"[ID: {cliente.get_id()}] {cliente.get_nombre():<20} {cliente.get_email():<25} {cliente.get_telefono()}")
        print(f"{'='*50}")

    # ========== MÉTODOS DE PEDIDOS ==========

    def crear_pedido(self, id_cliente, productos_ids):
        """
        Crea un nuevo pedido para un cliente.

        Args:
            id_cliente (int): ID del cliente que realiza el pedido
            productos_ids (list): Lista de IDs de productos en el pedido

        Returns:
            dict: Información del pedido creado o None si hay error
        """
        cliente = self.obtener_cliente_por_id(id_cliente)
        if not cliente:
            print(f"Error: Cliente con ID {id_cliente} no existe")
            return None

        # Validar que todos los productos existan y estén disponibles
        productos_pedido = []
        total = 0

        for id_producto in productos_ids:
            producto = self.obtener_producto_por_id(id_producto)
            if not producto:
                print(f"Error: Producto con ID {id_producto} no existe")
                return None
            if not producto.is_disponible():
                print(f"Error: Producto '{producto.get_nombre()}' no disponible")
                return None
            productos_pedido.append(producto)
            total += producto.get_precio()

        # Crear el pedido
        self.contador_pedidos += 1
        pedido = {
            'numero': self.contador_pedidos,
            'cliente_id': id_cliente,
            'cliente_nombre': cliente.get_nombre(),
            'productos': [(p.get_id(), p.get_nombre(), p.get_precio()) for p in productos_pedido],
            'total': total
        }

        self.pedidos.append(pedido)
        cliente.agregar_pedido(self.contador_pedidos)

        print(f"✓ Pedido #{self.contador_pedidos} creado exitosamente")
        return pedido

    def listar_pedidos(self):
        """Muestra todos los pedidos realizados."""
        if not self.pedidos:
            print("\n⚠ No hay pedidos registrados")
            return

        print(f"\n{'='*65}")
        print(f"PEDIDOS REALIZADOS")
        print(f"{'='*65}")
        for pedido in self.pedidos:
            print(f"\nPedido #{pedido['numero']}")
            print(f"Cliente: {pedido['cliente_nombre']} (ID: {pedido['cliente_id']})")
            print(f"Productos:")
            for id_prod, nombre_prod, precio_prod in pedido['productos']:
                print(f"  - {nombre_prod:<20} ${precio_prod:.2f}")
            print(f"Total: ${pedido['total']:.2f}")
        print(f"{'='*65}")

    def obtener_resumen_restaurante(self):
        """Muestra un resumen general del restaurante."""
        print(f"\n{'='*50}")
        print(f"RESUMEN DEL RESTAURANTE: {self.nombre}")
        print(f"{'='*50}")
        print(f"Dirección: {self.direccion}")
        print(f"Total de productos: {len(self.productos)}")
        print(f"Total de clientes: {len(self.clientes)}")
        print(f"Total de pedidos: {len(self.pedidos)}")

        if self.pedidos:
            total_ingresos = sum(p['total'] for p in self.pedidos)
            print(f"Ingresos totales: ${total_ingresos:.2f}")

        print(f"{'='*50}")

