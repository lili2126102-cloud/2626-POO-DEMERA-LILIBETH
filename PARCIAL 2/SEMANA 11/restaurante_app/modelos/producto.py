# -*- coding: utf-8 -*-

class Producto:
    """
    Clase que representa un producto del restaurante.
    Aplica encapsulación mediante propiedades (@property y @setter) para
    controlar la lectura y modificación de los atributos con validaciones.
    Incluye un atributo de stock para registrar las cantidades disponibles.
    """

    def __init__(self, codigo: str, nombre: str, categoria: str, precio: float, stock: int = 0) -> None:
        """
        Constructor de la clase Producto.
        Inicia los atributos a través de sus setters para asegurar que se
        ejecuten las validaciones correspondientes desde la instanciación.
        """
        self.codigo = codigo
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio
        self.stock = stock

    # --- Propiedad: codigo ---
    @property
    def codigo(self) -> str:
        """Getter para obtener el código del producto."""
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        """Setter para validar y asignar el código del producto."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El código del producto no puede estar vacío.")
        self._codigo = valor.strip()

    # --- Propiedad: nombre ---
    @property
    def nombre(self) -> str:
        """Getter para obtener el nombre del producto."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Setter para validar y asignar el nombre del producto."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._nombre = valor.strip()

    # --- Propiedad: categoria ---
    @property
    def categoria(self) -> str:
        """Getter para obtener la categoría del producto."""
        return self._categoria

    @categoria.setter
    def categoria(self, valor: str) -> None:
        """Setter para validar y asignar la categoría del producto."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La categoría del producto no puede estar vacía.")
        self._categoria = valor.strip()

    # --- Propiedad: precio ---
    @property
    def precio(self) -> float:
        """Getter para obtener el precio del producto."""
        return self._precio

    @precio.setter
    def precio(self, valor: float) -> None:
        """Setter para validar y asignar el precio del producto."""
        try:
            valor_num = float(valor)
        except (ValueError, TypeError):
            raise ValueError("El precio debe ser un valor numérico válido.")
        
        if valor_num <= 0:
            raise ValueError("El precio del producto debe ser estrictamente mayor que cero.")
        self._precio = valor_num

    # --- Propiedad: stock ---
    @property
    def stock(self) -> int:
        """Getter para obtener el stock del producto."""
        return self._stock

    @stock.setter
    def stock(self, valor: int) -> None:
        """Setter para validar y asignar el stock del producto, impidiendo que sea negativo."""
        try:
            valor_num = int(valor)
        except (ValueError, TypeError):
            raise ValueError("El stock debe ser un número entero válido.")
        
        if valor_num < 0:
            raise ValueError("El stock del producto no puede ser negativo.")
        self._stock = valor_num

    def vender(self, cantidad: int) -> None:
        """
        Disminuye la cantidad de stock disponible según lo solicitado.
        Valida que la cantidad sea válida y que haya suficiente disponibilidad.
        """
        try:
            cantidad_num = int(cantidad)
        except (ValueError, TypeError):
            raise ValueError("La cantidad a vender debe ser un número entero válido.")
        
        if cantidad_num <= 0:
            raise ValueError("La cantidad a vender debe ser estrictamente mayor que cero.")
        
        if self._stock < cantidad_num:
            raise ValueError(f"Stock insuficiente. Stock disponible: {self._stock}, solicitado: {cantidad_num}.")
        
        self.stock = self._stock - cantidad_num

    def mostrar_informacion(self) -> None:
        """
        Muestra en consola la información detallada del producto.
        """
        print(f"Código: {self.codigo}")
        print(f"Nombre: {self.nombre}")
        print(f"Categoría: {self.categoria}")
        print(f"Precio: ${self.precio:.2f}")
        print(f"Stock: {self.stock}")

    def to_dict(self) -> dict:
        """
        Convierte el objeto Producto en un diccionario para serialización JSON.
        """
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "stock": self.stock
        }

    @classmethod
    def from_dict(cls, datos: dict) -> 'Producto':
        """
        Reconstruye un objeto Producto a partir de un diccionario de datos.
        Lanza KeyError si falta alguna de las claves esperadas.
        Lanza ValueError si los datos no pasan las validaciones de la clase.
        """
        for clave in ["codigo", "nombre", "categoria", "precio", "stock"]:
            if clave not in datos:
                raise KeyError(f"Clave faltante '{clave}' en los datos del producto.")
        
        return cls(
            codigo=datos["codigo"],
            nombre=datos["nombre"],
            categoria=datos["categoria"],
            precio=datos["precio"],
            stock=datos["stock"]
        )
