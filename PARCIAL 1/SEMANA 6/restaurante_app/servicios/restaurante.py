from modelos.producto import Producto

class Restaurante:
    """
    Clase de servicio encargada de administrar una lista de productos registrados
    y mostrar la información de forma organizada.
    """
    def __init__(self, nombre_establecimiento: str = "El Gran Sabor"):
        """
        Constructor de la clase Restaurante.
        
        :param nombre_establecimiento: Nombre comercial del restaurante.
        """
        self.nombre_establecimiento = nombre_establecimiento
        # Lista que almacenará objetos de tipo Producto (Platillo y Bebida)
        self.productos = []

    def agregar_producto(self, producto: Producto) -> None:
        """
        Registra un nuevo producto (platillo o bebida) en la lista del restaurante.
        
        :param producto: Objeto instancia de Producto (o sus clases hijas).
        """
        self.productos.append(producto)
        print(f"[OK] Producto '{producto.nombre}' registrado con exito.")

    def mostrar_productos(self) -> None:
        """
        Recorre la lista de productos y ejecuta mostrar_informacion().
        Demuestra POLIMORFISMO, ya que cada objeto ejecuta su propio método
        mostrar_informacion() dependiendo de si es un Platillo o una Bebida.
        """
        print("\n" + "=" * 45)
        print(f" MENÚ DE: {self.nombre_establecimiento.upper()} ")
        print("=" * 45)
        
        if not self.productos:
            print("No hay productos registrados en el menú actualmente.")
            return

        for indice, producto in enumerate(self.productos, start=1):
            print(f"Nro {indice}:")
            # Llamada polimórfica: se ejecuta la versión del método correspondiente al tipo del objeto
            producto.mostrar_informacion()
            
        print("=" * 45 + "\n")
