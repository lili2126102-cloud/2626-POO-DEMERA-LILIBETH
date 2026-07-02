"""
Módulo que define la clase Cliente para representar a los clientes
del restaurante.
"""


class Cliente:
    """
    Clase que representa a un cliente del restaurante.

    Atributos:
        id (int): Identificador único del cliente
        nombre (str): Nombre completo del cliente
        email (str): Correo electrónico del cliente
        telefono (str): Número de teléfono del cliente
        pedidos_realizados (list): Lista de pedidos realizados por el cliente
    """

    # Variable de clase para controlar el contador de IDs
    contador_clientes = 0

    def __init__(self, nombre, email, telefono):
        """
        Inicializa una instancia de Cliente.

        Args:
            nombre (str): Nombre completo del cliente
            email (str): Correo electrónico del cliente
            telefono (str): Número de teléfono del cliente
        """
        Cliente.contador_clientes += 1
        self.id = Cliente.contador_clientes
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
        self.pedidos_realizados = []

    def get_id(self):
        """Retorna el ID del cliente."""
        return self.id

    def get_nombre(self):
        """Retorna el nombre del cliente."""
        return self.nombre

    def get_email(self):
        """Retorna el email del cliente."""
        return self.email

    def get_telefono(self):
        """Retorna el teléfono del cliente."""
        return self.telefono

    def set_email(self, nuevo_email):
        """
        Actualiza el email del cliente.

        Args:
            nuevo_email (str): Nuevo email del cliente
        """
        if "@" in nuevo_email:
            self.email = nuevo_email
        else:
            print("Error: Email inválido")

    def set_telefono(self, nuevo_telefono):
        """
        Actualiza el teléfono del cliente.

        Args:
            nuevo_telefono (str): Nuevo teléfono del cliente
        """
        self.telefono = nuevo_telefono

    def agregar_pedido(self, numero_pedido):
        """
        Registra un nuevo pedido realizado por el cliente.

        Args:
            numero_pedido (int): Número del pedido
        """
        self.pedidos_realizados.append(numero_pedido)

    def obtener_pedidos(self):
        """Retorna la lista de pedidos realizados por el cliente."""
        return self.pedidos_realizados

    def contar_pedidos(self):
        """Retorna la cantidad de pedidos realizados por el cliente."""
        return len(self.pedidos_realizados)

    def __str__(self):
        """Retorna una representación en texto del cliente."""
        return f"Cliente: {self.nombre} (ID: {self.id}) | Email: {self.email} | Teléfono: {self.telefono}"

    def mostrar_informacion(self):
        """Muestra la información del cliente de forma formateada."""
        print(f"\n{'='*50}")
        print(f"ID Cliente: {self.id}")
        print(f"Nombre: {self.nombre}")
        print(f"Email: {self.email}")
        print(f"Teléfono: {self.telefono}")
        print(f"Cantidad de pedidos: {self.contar_pedidos()}")
        if self.pedidos_realizados:
            print(f"Pedidos realizados: {self.pedidos_realizados}")
        print(f"{'='*50}")

