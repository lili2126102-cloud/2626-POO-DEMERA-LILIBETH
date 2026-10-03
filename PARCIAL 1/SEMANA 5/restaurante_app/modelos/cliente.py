# Clase Cliente - Representa un cliente registrado en el restaurante

class Cliente:
    """
    Clase que representa un cliente del restaurante.
    
    Atributos:
        - nombre: nombre completo del cliente (str)
        - correo: correo electrónico del cliente (str)
        - telefono: número de teléfono de contacto (str)
        - es_miembro: indica si el cliente es miembro frecuente (bool)
        - cantidad_visitas: número de veces que ha visitado (int)
    """
    
    def __init__(
        self, 
        nombre: str, 
        correo: str, 
        telefono: str, 
        es_miembro: bool = False,
        cantidad_visitas: int = 0
    ):
        """Constructor que inicializa los atributos del cliente."""
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.es_miembro = es_miembro
        self.cantidad_visitas = cantidad_visitas
    
    def __str__(self) -> str:
        """Representación en texto del cliente."""
        estado_miembro = "Miembro" if self.es_miembro else "Cliente regular"
        return (f"Cliente: {self.nombre} | Email: {self.correo} | "
                f"Teléfono: {self.telefono} | {estado_miembro} | "
                f"Visitas: {self.cantidad_visitas}")
    
    def registrar_visita(self) -> None:
        """Incrementa el contador de visitas del cliente."""
        self.cantidad_visitas += 1
    
    def convertir_a_miembro(self) -> None:
        """Convierte al cliente en miembro frecuente."""
        if not self.es_miembro:
            self.es_miembro = True
    
    def obtener_informacion_contacto(self) -> str:
        """Retorna la información de contacto del cliente."""
        return f"{self.nombre} - Email: {self.correo} - Teléfono: {self.telefono}"
