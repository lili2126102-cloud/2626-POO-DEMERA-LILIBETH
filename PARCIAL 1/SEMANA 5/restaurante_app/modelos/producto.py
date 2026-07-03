# Clase Producto - Representa un producto disponible en el restaurante

class Producto:
    """
    Clase que representa un producto del restaurante.
    
    Atributos:
        - nombre: nombre descriptivo del producto (str)
        - precio: precio del producto en dólares (float)
        - cantidad_disponible: cantidad en inventario (int)
        - es_disponible: indica si el producto está disponible (bool)
    """
    
    def __init__(
        self, 
        nombre: str, 
        precio: float, 
        cantidad_disponible: int, 
        es_disponible: bool = True
    ):
        """Constructor que inicializa los atributos del producto."""
        self.nombre = nombre
        self.precio = precio
        self.cantidad_disponible = cantidad_disponible
        self.es_disponible = es_disponible
    
    def __str__(self) -> str:
        """Representación en texto del producto."""
        estado = "Disponible" if self.es_disponible else "No disponible"
        return (f"Producto: {self.nombre} | Precio: ${self.precio:.2f} | "
                f"Stock: {self.cantidad_disponible} | Estado: {estado}")
    
    def reducir_stock(self, cantidad: int) -> bool:
        """
        Reduce el stock del producto si hay disponibilidad.
        
        Args:
            cantidad: cantidad a reducir
            
        Returns:
            True si la reducción fue exitosa, False en caso contrario
        """
        if cantidad <= self.cantidad_disponible and self.es_disponible:
            self.cantidad_disponible -= cantidad
            return True
        return False
    
    def aumentar_stock(self, cantidad: int) -> None:
        """Aumenta el stock del producto."""
        self.cantidad_disponible += cantidad
    
    def cambiar_disponibilidad(self, es_disponible: bool) -> None:
        """Cambia el estado de disponibilidad del producto."""
        self.es_disponible = es_disponible
