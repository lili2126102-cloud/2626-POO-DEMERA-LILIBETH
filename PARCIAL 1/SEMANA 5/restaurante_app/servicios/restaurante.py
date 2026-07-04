# Clase Restaurante - Gestiona productos y clientes del restaurante

from modelos.producto import Producto
from modelos.cliente import Cliente
from typing import List


class Restaurante:
    """
    Clase que representa un restaurante y gestiona sus operaciones.
    
    Atributos:
        - nombre: nombre del restaurante (str)
        - ubicacion: dirección del restaurante (str)
        - productos: lista de productos disponibles (List[Producto])
        - clientes: lista de clientes registrados (List[Cliente])
        - año_fundacion: año en que se fundó el restaurante (int)
    """
    
    def __init__(
        self, 
        nombre: str, 
        ubicacion: str, 
        año_fundacion: int
    ):
        """Constructor que inicializa los atributos del restaurante."""
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.año_fundacion = año_fundacion
        self.productos: List[Producto] = []
        self.clientes: List[Cliente] = []
    
    def agregar_producto(self, producto: Producto) -> None:
        """Agrega un nuevo producto al restaurante."""
        self.productos.append(producto)
    
    def agregar_cliente(self, cliente: Cliente) -> None:
        """Registra un nuevo cliente en el restaurante."""
        self.clientes.append(cliente)
    
    def mostrar_productos(self) -> None:
        """Muestra la lista de todos los productos disponibles."""
        print(f"\n--- Productos disponibles en {self.nombre} ---")
        if not self.productos:
            print("No hay productos registrados.")
            return
        
        for producto in self.productos:
            print(f"  • {producto}")
    
    def mostrar_clientes(self) -> None:
        """Muestra la lista de todos los clientes registrados."""
        print(f"\n--- Clientes registrados en {self.nombre} ---")
        if not self.clientes:
            print("No hay clientes registrados.")
            return
        
        for cliente in self.clientes:
            print(f"  • {cliente}")
    
    def contar_productos(self) -> int:
        """Retorna la cantidad total de productos."""
        return len(self.productos)
    
    def contar_clientes(self) -> int:
        """Retorna la cantidad total de clientes."""
        return len(self.clientes)
    
    def contar_miembros(self) -> int:
        """Retorna la cantidad de clientes que son miembros."""
        miembros = [cliente for cliente in self.clientes if cliente.es_miembro]
        return len(miembros)
    
    def obtener_informacion_restaurante(self) -> str:
        """Retorna información general del restaurante."""
        return (f"Restaurante: {self.nombre}\n"
                f"Ubicación: {self.ubicacion}\n"
                f"Año de fundación: {self.año_fundacion}\n"
                f"Total de productos: {self.contar_productos()}\n"
                f"Total de clientes: {self.contar_clientes()}\n"
                f"Miembros frecuentes: {self.contar_miembros()}")
