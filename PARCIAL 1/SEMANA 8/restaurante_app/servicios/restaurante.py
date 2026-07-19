# -*- coding: utf-8 -*-
from modelos.producto import Producto
from modelos.cliente import Cliente

class Restaurante:
    """
    Clase de servicio encargada de administrar las colecciones de productos y clientes.
    Aplica el Principio de Responsabilidad Única (SRP) al separar la lógica de negocio,
    las validaciones de unicidad y la persistencia en memoria de la interacción por consola.
    """

    def __init__(self, nombre_establecimiento: str = "El Gran Sabor SOLID") -> None:
        """
        Constructor del servicio Restaurante.
        Inicializa colecciones vacías para productos y clientes.
        """
        self.nombre_establecimiento: str = nombre_establecimiento
        self.productos: list[Producto] = []
        self.clientes: list[Cliente] = []

    def registrar_producto(self, producto: Producto) -> None:
        """
        Registra un objeto Producto o Bebida en la colección de productos.
        Aplica validación para evitar códigos de producto duplicados.
        """
        # Validar duplicación de código
        for p in self.productos:
            if p.codigo == producto.codigo:
                raise ValueError(f"Ya existe un producto o bebida registrado con el código '{producto.codigo}'.")
        
        self.productos.append(producto)

    def listar_productos(self) -> None:
        """
        Muestra la lista de productos registrados.
        Aplica Polimorfismo y el Principio de Sustitución de Liskov (LSP) al invocar
        el método común mostrar_informacion() para todos los elementos sin preguntar
        su tipo concreto (Producto o Bebida) ni usar estructuras condicionales para ello.
        """
        if not self.productos:
            print("\n\033[93m[!] No hay productos registrados en el menú actualmente.\033[0m")
            return

        print("\n\033[96m==================================================")
        print(f"        MENÚ DE PRODUCTOS - {self.nombre_establecimiento.upper()}")
        print("==================================================\033[0m")
        for idx, producto in enumerate(self.productos, start=1):
            print(f"\n\033[94mNro {idx:02d}:\033[0m")
            # Conexión polimórfica común
            producto.mostrar_informacion()
            print("\033[90m" + "-" * 50 + "\033[0m")
        print("\033[96m==================================================\033[0m")

    def registrar_cliente(self, cliente: Cliente) -> None:
        """
        Registra un objeto Cliente en la colección.
        Aplica validación para evitar identificaciones de clientes duplicadas.
        """
        # Validar duplicación de identificación
        for c in self.clientes:
            if c.identificacion == cliente.identificacion:
                raise ValueError(f"Ya existe un cliente registrado con la identificación '{cliente.identificacion}'.")
        
        self.clientes.append(cliente)

    def listar_clientes(self) -> None:
        """
        Muestra la lista de clientes registrados, llamando al método mostrar_informacion()
        de cada instancia de Cliente.
        """
        if not self.clientes:
            print("\n\033[93m[!] No hay clientes registrados en el sistema actualmente.\033[0m")
            return

        print("\n\033[96m==================================================")
        print("             CLIENTES REGISTRADOS")
        print("==================================================\033[0m")
        for idx, cliente in enumerate(self.clientes, start=1):
            print(f"\n\033[94mNro {idx:02d}:\033[0m")
            cliente.mostrar_informacion()
            print("\033[90m" + "-" * 50 + "\033[0m")
        print("\033[96m==================================================\033[0m")
