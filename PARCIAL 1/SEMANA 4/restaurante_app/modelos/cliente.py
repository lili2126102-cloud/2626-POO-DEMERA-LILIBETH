# Clase Cliente - representa una persona que realiza o consume un pedido en el restaurante

class Cliente:
    """
    Representa un cliente del restaurante LYDIA.
    Contiene información personal del cliente como nombre, contacto y afiliación.
    """

    # Variable de clase para contar clientes registrados
    cantidad_clientes = 0

    def __init__(self, nombre, correo, telefono):
        """
        Constructor de la clase Cliente.
        Registra automáticamente el cliente incrementando el contador.

        Parámetros:
        - nombre: nombre completo del cliente (str)
        - correo: correo electrónico del cliente (str)
        - telefono: número de teléfono del cliente (str)
        """
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.cliente_id = Cliente.cantidad_clientes + 1
        Cliente.cantidad_clientes += 1
        self.pedidos_realizados = 0

    def __str__(self):
        """
        Retorna una representación en texto del cliente.
        Muestra ID, nombre, correo y teléfono.
        """
        return f"Cliente #{self.cliente_id}: {self.nombre} | Email: {self.correo} | Tel: {self.telefono}"

    def registrar_pedido(self):
        """
        Incrementa el contador de pedidos realizados por el cliente.
        Se llama cada vez que el cliente hace un pedido.
        """
        self.pedidos_realizados += 1
        return f"Pedido registrado. Total de pedidos: {self.pedidos_realizados}"

    def obtener_informacion(self):
        """
        Retorna información detallada del cliente incluidos sus pedidos.
        """
        return f"Nombre: {self.nombre} | ID: {self.cliente_id} | Pedidos realizados: {self.pedidos_realizados}"

