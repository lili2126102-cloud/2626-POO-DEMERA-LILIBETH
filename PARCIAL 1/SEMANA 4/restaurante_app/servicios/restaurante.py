# Clase Restaurante - gestiona productos, clientes y operaciones del restaurante

from modelos.producto import Producto
from modelos.cliente import Cliente

class Restaurante:
    """
    Gestiona las operaciones principales del restaurante LYDIA.
    Administra el registro de productos y clientes del sistema.
    """

    def __init__(self, nombre, ubicacion):
        """
        Constructor de la clase Restaurante.
        Inicializa el restaurante con listas vacías para productos y clientes.

        Parámetros:
        - nombre: nombre del restaurante (str)
        - ubicacion: ubicación o dirección del restaurante (str)
        """
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.productos = []  # Lista de productos disponibles
        self.clientes = []   # Lista de clientes registrados

    def __str__(self):
        """
        Retorna una representación en texto del restaurante.
        Muestra nombre, ubicación y cantidad de productos y clientes.
        """
        return f"Restaurante '{self.nombre}' | Ubicación: {self.ubicacion} | Productos: {len(self.productos)} | Clientes: {len(self.clientes)}"

    def agregar_producto(self, producto):
        """
        Agrega un producto al catálogo del restaurante.

        Parámetro:
        - producto: objeto de tipo Producto a agregar
        """
        if isinstance(producto, Producto):
            self.productos.append(producto)
            return f"✓ Producto '{producto.nombre}' agregado exitosamente"
        else:
            return "Error: El objeto no es una instancia de Producto"

    def agregar_cliente(self, cliente):
        """
        Registra un cliente en el sistema del restaurante.

        Parámetro:
        - cliente: objeto de tipo Cliente a registrar
        """
        if isinstance(cliente, Cliente):
            self.clientes.append(cliente)
            return f"✓ Cliente '{cliente.nombre}' registrado exitosamente"
        else:
            return "Error: El objeto no es una instancia de Cliente"

    def listar_productos(self):
        """
        Lista todos los productos disponibles en el restaurante.
        Retorna un string con la información de cada producto.
        """
        if not self.productos:
            return "No hay productos registrados"

        listado = f"\n{'='*60}\nCATÁLOGO DE PRODUCTOS - {self.nombre}\n{'='*60}\n"
        for i, producto in enumerate(self.productos, 1):
            listado += f"{i}. {producto}\n"
        listado += "="*60
        return listado

    def listar_clientes(self):
        """
        Lista todos los clientes registrados en el sistema.
        Retorna un string con la información de cada cliente.
        """
        if not self.clientes:
            return "No hay clientes registrados"

        listado = f"\n{'='*60}\nCLIENTES REGISTRADOS - {self.nombre}\n{'='*60}\n"
        for cliente in self.clientes:
            listado += f"{cliente}\n"
        listado += "="*60
        return listado

    def buscar_producto(self, nombre):
        """
        Busca un producto por nombre en el catálogo.

        Parámetro:
        - nombre: nombre del producto a buscar (str)

        Retorna:
        - El objeto Producto si lo encuentra, None en caso contrario
        """
        for producto in self.productos:
            if producto.nombre.lower() == nombre.lower():
                return producto
        return None

    def buscar_cliente(self, nombre):
        """
        Busca un cliente por nombre en el sistema.

        Parámetro:
        - nombre: nombre del cliente a buscar (str)

        Retorna:
        - El objeto Cliente si lo encuentra, None en caso contrario
        """
        for cliente in self.clientes:
            if cliente.nombre.lower() == nombre.lower():
                return cliente
        return None

    def obtener_estadisticas(self):
        """
        Retorna estadísticas del restaurante.
        """
        total_productos = len(self.productos)
        productos_disponibles = sum(1 for p in self.productos if p.disponible)
        total_clientes = len(self.clientes)

        estadisticas = f"\n{'='*60}\nESTADÍSTICAS DEL RESTAURANTE {self.nombre.upper()}\n{'='*60}\n"
        estadisticas += f"Total de productos en catálogo: {total_productos}\n"
        estadisticas += f"Productos disponibles: {productos_disponibles}\n"
        estadisticas += f"Total de clientes registrados: {total_clientes}\n"
        estadisticas += "="*60

        return estadisticas

