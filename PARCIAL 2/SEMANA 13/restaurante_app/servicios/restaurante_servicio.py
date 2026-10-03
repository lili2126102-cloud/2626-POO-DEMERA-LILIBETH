# -*- coding: utf-8 -*-
from typing import List, Optional
from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    """
    Servicio principal de lógica del restaurante.
    Recibe la información cargada desde el ArchivoServicio, transforma los
    datos en objetos de dominio (Producto, Usuario) y proporciona las
    operaciones requeridas por la interfaz gráfica:
    - Validación de acceso (login simulado)
    - Consulta y listado de productos
    - Consulta y listado de usuarios
    - Cálculo de métricas y cantidades
    """

    def __init__(self, archivo_servicio: ArchivoServicio) -> None:
        """
        Inicializa el servicio inyectando la dependencia de ArchivoServicio.
        """
        self.archivo_servicio = archivo_servicio
        self._productos: List[Producto] = []
        self._usuarios: List[Usuario] = []

    @property
    def productos(self) -> List[Producto]:
        """Retorna una copia superficial de la lista de productos."""
        return list(self._productos)

    @property
    def usuarios(self) -> List[Usuario]:
        """Retorna una copia superficial de la lista de usuarios."""
        return list(self._usuarios)

    def cargar_datos(self) -> None:
        """
        Carga la información desde los archivos JSON mediante ArchivoServicio,
        instancia los modelos Producto y Usuario, y los almacena en memoria.
        """
        self._cargar_productos()
        self._cargar_usuarios()

    def _cargar_productos(self) -> None:
        """Lee y convierte los datos crudos de productos a objetos Producto."""
        self._productos.clear()
        try:
            datos = self.archivo_servicio.cargar_datos_productos()
            for item in datos:
                try:
                    producto = Producto.from_dict(item)
                    self._productos.append(producto)
                except (KeyError, ValueError) as e:
                    print(f"[Aviso] Producto omitido por datos inválidos: {e}")
        except Exception as e:
            print(f"[Error] No fue posible cargar los productos: {e}")

    def _cargar_usuarios(self) -> None:
        """Lee y convierte los datos crudos de usuarios a objetos Usuario."""
        self._usuarios.clear()
        try:
            datos = self.archivo_servicio.cargar_datos_usuarios()
            for item in datos:
                try:
                    usuario = Usuario.from_dict(item)
                    self._usuarios.append(usuario)
                except (KeyError, ValueError) as e:
                    print(f"[Aviso] Usuario omitido por datos inválidos: {e}")
        except Exception as e:
            print(f"[Error] No fue posible cargar los usuarios: {e}")

    # === Operaciones de Negocio para la UI ===

    def validar_acceso(self, identificador: str, clave: str) -> Optional[Usuario]:
        """
        Valida las credenciales ingresadas en la pantalla de acceso (LoginView).
        Permite ingresar mediante la cédula/identificación o mediante el correo electrónico.
        Retorna el objeto Usuario correspondiente si las credenciales coinciden;
        retorna None en caso de credenciales incorrectas o inexistentes.
        """
        if not identificador or not clave:
            return None

        id_limpio = identificador.strip().lower()
        clave_limpia = clave.strip()

        for usuario in self._usuarios:
            coincide_identificacion = usuario.identificacion.strip().lower() == id_limpio
            coincide_correo = usuario.correo.strip().lower() == id_limpio

            if (coincide_identificacion or coincide_correo) and usuario.validar_credencial(clave_limpia):
                return usuario

        return None

    def listar_productos(self) -> List[Producto]:
        """
        Retorna la lista de todos los productos registrados.
        Las vistas invocan este método en lugar de consultar los archivos directamente.
        """
        return list(self._productos)

    def listar_usuarios(self) -> List[Usuario]:
        """
        Retorna la lista de todos los usuarios registrados en el sistema.
        """
        return list(self._usuarios)

    def obtener_cantidad_productos(self) -> int:
        """Retorna el número total de productos disponibles en el catálogo."""
        return len(self._productos)

    def obtener_cantidad_usuarios(self) -> int:
        """Retorna el número total de usuarios registrados."""
        return len(self._usuarios)

    def obtener_total_stock(self) -> int:
        """Calcula la suma del stock disponible en todos los productos."""
        return sum(p.stock for p in self._productos)

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        """Busca y retorna un producto por su código único."""
        codigo_buscado = codigo.strip().lower()
        for p in self._productos:
            if p.codigo.strip().lower() == codigo_buscado:
                return p
        return None

    def buscar_usuario(self, identificacion: str) -> Optional[Usuario]:
        """Busca y retorna un usuario por su número de identificación."""
        id_buscado = identificacion.strip().lower()
        for u in self._usuarios:
            if u.identificacion.strip().lower() == id_buscado:
                return u
        return None
