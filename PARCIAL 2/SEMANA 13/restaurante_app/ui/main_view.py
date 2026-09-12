# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable
from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio

class MainView(ttk.Frame):
    """
    Panel principal de la aplicación del restaurante.
    Se despliega únicamente después de un acceso exitoso y permite:
    - Consultar los productos registrados en el inventario.
    - Consultar los usuarios registrados en el sistema.
    - Visualizar opciones futuras identificadas como pendientes (Ventas).
    - Cerrar sesión para regresar a la vista de login dentro de la misma ventana.
    
    Todas las consultas de datos se realizan a través de RestauranteServicio,
    sin acceder directamente a los archivos locales JSON.
    """

    def __init__(
        self,
        parent: tk.Widget,
        usuario_autenticado: Usuario,
        restaurante_servicio: RestauranteServicio,
        on_cerrar_sesion: Callable[[], None]
    ) -> None:
        """
        Inicializa el panel principal.
        
        :param parent: Contenedor padre de Tkinter.
        :param usuario_autenticado: Instancia del Usuario que inició sesión.
        :param restaurante_servicio: Servicio que administra la información.
        :param on_cerrar_sesion: Callback para volver a la pantalla de Login.
        """
        super().__init__(parent)
        self.usuario_autenticado = usuario_autenticado
        self.restaurante_servicio = restaurante_servicio
        self.on_cerrar_sesion = on_cerrar_sesion

        self._configurar_interfaz()
        self.cargar_datos_vistas()

    def _configurar_interfaz(self) -> None:
        """Construye los elementos de la interfaz principal con pestañas de navegación."""
        self.pack(fill="both", expand=True)

        # 1. Barra Superior (Header con Branding y Control de Sesión)
        header_frame = tk.Frame(self, bg="#1A365D", height=60)
        header_frame.pack(fill="x", side="top")

        lbl_logo = tk.Label(
            header_frame,
            text="🍽️  RESTAURANTE GOURMET",
            font=("Segoe UI", 13, "bold"),
            fg="white",
            bg="#1A365D",
            padx=15,
            pady=10
        )
        lbl_logo.pack(side="left")

        # Contenedor derecho del header (Datos de usuario y botón Cerrar Sesión)
        user_panel = tk.Frame(header_frame, bg="#1A365D")
        user_panel.pack(side="right", padx=15, pady=8)

        lbl_usuario = tk.Label(
            user_panel,
            text=f"Conectado como: {self.usuario_autenticado.nombre}",
            font=("Segoe UI", 9, "bold"),
            fg="#E2E8F0",
            bg="#1A365D"
        )
        lbl_usuario.pack(side="left", padx=(0, 15))

        btn_salir = tk.Button(
            user_panel,
            text="Cerrar Sesión",
            font=("Segoe UI", 9, "bold"),
            bg="#E53E3E",
            fg="white",
            activebackground="#C53030",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=3,
            command=self._confirmar_cierre_sesion
        )
        btn_salir.pack(side="left")

        # 2. Contenedor de Pestañas (Notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=15, pady=12)

        # Crear frames para cada pestaña
        self.tab_productos = ttk.Frame(self.notebook, padding=10)
        self.tab_usuarios = ttk.Frame(self.notebook, padding=10)
        self.tab_ventas = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.tab_productos, text=" 🍲 Productos Registrados ")
        self.notebook.add(self.tab_usuarios, text=" 👥 Usuarios Registrados ")
        self.notebook.add(self.tab_ventas, text=" 🧾 Ventas (Pendiente) ")

        # Configurar el contenido de cada pestaña
        self._construir_pestana_productos()
        self._construir_pestana_usuarios()
        self._construir_pestana_ventas()

        # 3. Barra de Estado Inferior
        status_bar = ttk.Frame(self, padding=(15, 4))
        status_bar.pack(fill="x", side="bottom")

        lbl_status = ttk.Label(
            status_bar,
            text="Semana 13 • POO UEA — Arquitectura en Capas (Modelos, Servicios, UI, Persistencia)",
            font=("Segoe UI", 8),
            foreground="#718096"
        )
        lbl_status.pack(side="left")

    # === Pestaña 1: Productos Registrados ===

    def _construir_pestana_productos(self) -> None:
        """Construye la vista de tabla para los productos cargados."""
        # Barra superior con resumen y botón de recarga
        top_bar = ttk.Frame(self.tab_productos)
        top_bar.pack(fill="x", pady=(0, 8))

        self.lbl_resumen_productos = ttk.Label(
            top_bar,
            text="Cargando productos...",
            font=("Segoe UI", 10, "bold")
        )
        self.lbl_resumen_productos.pack(side="left", anchor="w")

        btn_recargar = ttk.Button(
            top_bar,
            text="🔄 Actualizar Lista",
            command=self.cargar_productos
        )
        btn_recargar.pack(side="right")

        # Tabla de productos (Treeview)
        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tree_productos = ttk.Treeview(
            self.tab_productos,
            columns=columnas,
            show="headings",
            selectmode="browse",
            height=14
        )

        # Encabezados y anchos
        self.tree_productos.heading("codigo", text="Código")
        self.tree_productos.heading("nombre", text="Nombre del Producto")
        self.tree_productos.heading("categoria", text="Categoría")
        self.tree_productos.heading("precio", text="Precio ($)")
        self.tree_productos.heading("stock", text="Stock (uds)")

        self.tree_productos.column("codigo", width=90, anchor="center")
        self.tree_productos.column("nombre", width=220, anchor="w")
        self.tree_productos.column("categoria", width=130, anchor="center")
        self.tree_productos.column("precio", width=100, anchor="e")
        self.tree_productos.column("stock", width=100, anchor="center")

        # Scrollbar vertical
        scrollbar_prod = ttk.Scrollbar(
            self.tab_productos,
            orient="vertical",
            command=self.tree_productos.yview
        )
        self.tree_productos.configure(yscrollcommand=scrollbar_prod.set)

        self.tree_productos.pack(side="left", fill="both", expand=True)
        scrollbar_prod.pack(side="right", fill="y")

    # === Pestaña 2: Usuarios Registrados ===

    def _construir_pestana_usuarios(self) -> None:
        """Construye la vista de tabla para los usuarios registrados."""
        top_bar = ttk.Frame(self.tab_usuarios)
        top_bar.pack(fill="x", pady=(0, 8))

        self.lbl_resumen_usuarios = ttk.Label(
            top_bar,
            text="Cargando usuarios...",
            font=("Segoe UI", 10, "bold")
        )
        self.lbl_resumen_usuarios.pack(side="left", anchor="w")

        btn_recargar = ttk.Button(
            top_bar,
            text="🔄 Actualizar Lista",
            command=self.cargar_usuarios
        )
        btn_recargar.pack(side="right")

        # Tabla de usuarios
        columnas = ("identificacion", "nombre", "correo")
        self.tree_usuarios = ttk.Treeview(
            self.tab_usuarios,
            columns=columnas,
            show="headings",
            selectmode="browse",
            height=14
        )

        self.tree_usuarios.heading("identificacion", text="Identificación / Cédula")
        self.tree_usuarios.heading("nombre", text="Nombre Completo")
        self.tree_usuarios.heading("correo", text="Correo Electrónico")

        self.tree_usuarios.column("identificacion", width=150, anchor="center")
        self.tree_usuarios.column("nombre", width=230, anchor="w")
        self.tree_usuarios.column("correo", width=250, anchor="w")

        scrollbar_usr = ttk.Scrollbar(
            self.tab_usuarios,
            orient="vertical",
            command=self.tree_usuarios.yview
        )
        self.tree_usuarios.configure(yscrollcommand=scrollbar_usr.set)

        self.tree_usuarios.pack(side="left", fill="both", expand=True)
        scrollbar_usr.pack(side="right", fill="y")

    # === Pestaña 3: Ventas (Funcionalidad Pendiente) ===

    def _construir_pestana_ventas(self) -> None:
        """Presenta el módulo de ventas claramente identificado como funcionalidad pendiente."""
        contenedor = ttk.Frame(self.tab_ventas, padding=30)
        contenedor.pack(fill="both", expand=True)

        lbl_icono = ttk.Label(
            contenedor,
            text="⏳ 🧾",
            font=("Segoe UI Emoji", 36)
        )
        lbl_icono.pack(pady=(20, 10))

        lbl_titulo = ttk.Label(
            contenedor,
            text="Módulo de Ventas — Funcionalidad Pendiente",
            font=("Segoe UI", 14, "bold")
        )
        lbl_titulo.pack(pady=(0, 8))

        texto_explicativo = (
            "De acuerdo con las instrucciones pedagógicas de la Semana 13, en esta etapa se parte "
            "de una base gráfica simplificada con el fin de consolidar la arquitectura por capas "
            "(Modelos, Servicios, Vistas y Persistencia).\n\n"
            "El módulo transaccional de ventas, la facturación y la actualización de inventarios "
            "mediante interfaz gráfica se incorporarán de manera progresiva en los contenidos de las siguientes semanas."
        )

        lbl_descripcion = ttk.Label(
            contenedor,
            text=texto_explicativo,
            font=("Segoe UI", 10),
            wraplength=520,
            justify="center",
            foreground="#4A5568"
        )
        lbl_descripcion.pack(pady=(0, 20))

        # Cuadro informativo de evolución futura
        tarjeta_info = ttk.LabelFrame(contenedor, text=" Próximos incrementos del sistema ", padding=15)
        tarjeta_info.pack(fill="x", padx=40)

        roadmap = (
            "• Formulario interactivo para registrar nuevas ventas y órdenes.\n"
            "• Descuento automático de stock con validación en tiempo real.\n"
            "• Historial de compras asociadas a cada cliente registrado.\n"
            "• Generación de reportes de recaudación y facturación."
        )
        lbl_roadmap = ttk.Label(
            tarjeta_info,
            text=roadmap,
            font=("Segoe UI", 9),
            foreground="#2D3748",
            justify="left"
        )
        lbl_roadmap.pack(anchor="w")

    # === Lógica de Consulta y Carga de Datos desde RestauranteServicio ===

    def cargar_datos_vistas(self) -> None:
        """Carga los datos en ambas pestañas a través del servicio."""
        self.cargar_productos()
        self.cargar_usuarios()

    def cargar_productos(self) -> None:
        """
        Consulta los productos al RestauranteServicio y los muestra en la tabla.
        Demuestra la regla obligatoria: la vista solicita la información al servicio
        y NO lee directamente los archivos JSON.
        """
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)

        # Consulta al servicio
        productos = self.restaurante_servicio.listar_productos()
        total_stock = self.restaurante_servicio.obtener_total_stock()

        for prod in productos:
            self.tree_productos.insert(
                "",
                "end",
                values=(
                    prod.codigo,
                    prod.nombre,
                    prod.categoria,
                    f"${prod.precio:.2f}",
                    prod.stock
                )
            )

        self.lbl_resumen_productos.config(
            text=f"Total de productos en catálogo: {len(productos)}  |  Stock total acumulado: {total_stock} unidades"
        )

    def cargar_usuarios(self) -> None:
        """
        Consulta los usuarios al RestauranteServicio y los muestra en la tabla.
        """
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)

        # Consulta al servicio
        usuarios = self.restaurante_servicio.listar_usuarios()

        for usr in usuarios:
            self.tree_usuarios.insert(
                "",
                "end",
                values=(
                    usr.identificacion,
                    usr.nombre,
                    usr.correo
                )
            )

        self.lbl_resumen_usuarios.config(
            text=f"Total de usuarios registrados: {len(usuarios)}"
        )

    # === Control de Sesión ===

    def _confirmar_cierre_sesion(self) -> None:
        """Solicita confirmación al usuario antes de cerrar la sesión."""
        confirmado = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Está seguro de que desea salir del sistema y regresar a la pantalla de acceso?",
            parent=self
        )
        if confirmado:
            self.on_cerrar_sesion()
