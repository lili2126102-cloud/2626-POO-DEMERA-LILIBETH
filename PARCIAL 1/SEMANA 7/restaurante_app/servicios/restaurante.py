# -*- coding: utf-8 -*-
from modelos.producto import Producto
from modelos.cliente import Cliente

class Restaurante:
    """
    Clase de servicio encargada de administrar las listas de productos y clientes registrados.
    Actúa como la capa de lógica de negocio y persistencia en memoria del sistema.
    """

    def __init__(self, nombre_establecimiento: str = "El Gran Sabor"):
        """
        Constructor de la clase Restaurante.
        Inicializa las listas vacías para productos y clientes.
        """
        self.nombre_establecimiento = nombre_establecimiento
        self.productos: list[Producto] = []
        self.clientes: list[Cliente] = []

    # --- Métodos de Gestión de Productos ---

    def registrar_producto(self, producto: Producto) -> None:
        """
        Registra un objeto Producto en la lista del restaurante.
        """
        self.productos.append(producto)
        print(f"\n[OK] Producto '{producto.nombre}' registrado con éxito en el sistema.")

    def listar_productos(self) -> None:
        """
        Imprime en consola la lista completa de productos registrados,
        llamando al método mostrar_informacion() de cada uno.
        """
        if not self.productos:
            print("\n[!] No hay productos registrados en el menú actualmente.")
            return

        print("\n" + "=" * 50)
        print(f"        MENÚ DE PRODUCTOS - {self.nombre_establecimiento.upper()}")
        print("=" * 50)
        for idx, producto in enumerate(self.productos, start=1):
            print(f"\nNro {idx}:")
            producto.mostrar_informacion()
        print("\n" + "=" * 50)

    def buscar_producto(self, nombre: str) -> list[Producto]:
        """
        Busca productos en la lista que coincidan de forma parcial con el nombre buscado.
        Retorna una lista de productos encontrados.
        """
        nombre_busqueda = nombre.strip().lower()
        coincidencias = [p for p in self.productos if nombre_busqueda in p.nombre.lower()]
        return coincidencias

    # --- Métodos de Gestión de Clientes ---

    def registrar_cliente(self, cliente: Cliente) -> None:
        """
        Registra un objeto Cliente en la lista del restaurante.
        """
        self.clientes.append(cliente)
        print(f"\n[OK] Cliente '{cliente.nombre}' registrado con éxito en el sistema.")

    def listar_clientes(self) -> None:
        """
        Imprime en consola la lista de todos los clientes registrados.
        """
        if not self.clientes:
            print("\n[!] No hay clientes registrados en el sistema actualmente.")
            return

        print("\n" + "=" * 50)
        print("             LISTADO DE CLIENTES REGISTRADOS")
        print("=" * 50)
        for idx, cliente in enumerate(self.clientes, start=1):
            print(f"{idx:02d}. ID: {cliente.id_cliente:<10} | Nombre: {cliente.nombre:<20} | Correo: {cliente.correo}")
        print("=" * 50)

    def buscar_cliente(self, id_cliente: str) -> Cliente | None:
        """
        Busca un cliente específico por su identificador único (id_cliente).
        Retorna la instancia del Cliente si lo encuentra, de lo contrario None.
        """
        id_busqueda = id_cliente.strip().lower()
        for cliente in self.clientes:
            if cliente.id_cliente.strip().lower() == id_busqueda:
                return cliente
        return None
