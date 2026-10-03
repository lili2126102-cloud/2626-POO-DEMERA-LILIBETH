# -*- coding: utf-8 -*-
"""
Panel Principal - Restaurante App (Semana 15)
=============================================
Asignatura: Programación Orientada a Objetos (UEA)
Estudiante: Lilibeth Demera

Implementa la interfaz principal del sistema aplicando componentes y contenedores
de Tkinter/ttk, una paleta de colores pasteles, recursos gráficos de assets/
y el flujo completo de eventos para el registro de ventas:
USUARIO -> ACCIÓN -> BOTÓN con command= -> CALLBACK -> SERVICIO -> PERSISTENCIA -> RESPUESTA VISUAL.
"""

import os
import re
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional, Dict

from modelos.usuario import Usuario
from modelos.producto import Producto
from modelos.venta import Venta
from servicios.restaurante_servicio import RestauranteServicio


class MainView(ttk.Frame):
    """
    Panel integral de administración del restaurante.
    Organizado mediante contenedores jerárquicos:
    - Header superior con branding corporativo de assets/ y panel de sesión.
    - Pestañas de navegación (Notebook):
        1. Gestión de Productos (CRUD y Catálogo)
        2. Consulta de Usuarios
        3. Registro y Gestión de Ventas (Manejo de Eventos y Transacciones)
    - Barra de estado inferior con retroalimentación visual en tiempo real.
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
        :param usuario_autenticado: Instancia del Usuario autenticado.
        :param restaurante_servicio: Servicio del dominio.
        :param on_cerrar_sesion: Callback para retornar a LoginView.
        """
        super().__init__(parent)
        self.usuario_autenticado = usuario_autenticado
        self.restaurante_servicio = restaurante_servicio
        self.on_cerrar_sesion = on_cerrar_sesion

        # Mapeos internos para selección ágil en comboboxes de venta
        self._mapa_usuarios_combo: Dict[str, str] = {}
        self._mapa_productos_combo: Dict[str, str] = {}
        self._img_logo_header: Optional[tk.PhotoImage] = None

        self._configurar_interfaz()
        self.cargar_datos_vistas()

    def _configurar_interfaz(self) -> None:
        """Construye todos los contenedores y componentes de la vista principal."""
        self.pack(fill="both", expand=True)

        # ---------------------------------------------------------------------
        # 1. CONTENEDOR SUPERIOR: Header con colores pasteles y logo de assets/
        # ---------------------------------------------------------------------
        header_frame = tk.Frame(self, bg="#8FA4B5", height=60)  # Azul pizarra pastel
        header_frame.pack(fill="x", side="top")

        # Intentar cargar logotipo del header desde assets/
        directorio_app = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        ruta_logo_hdr = os.path.join(directorio_app, "assets", "logo_header.png")
        
        branding_box = tk.Frame(header_frame, bg="#8FA4B5")
        branding_box.pack(side="left", padx=14, pady=6)

        if os.path.exists(ruta_logo_hdr):
            try:
                self._img_logo_header = tk.PhotoImage(file=ruta_logo_hdr)
                lbl_logo_img = tk.Label(branding_box, image=self._img_logo_header, bg="#8FA4B5")
                lbl_logo_img.pack(side="left", padx=(0, 10))
            except Exception:
                pass

        lbl_logo = tk.Label(
            branding_box,
            text="RESTAURANTE GOURMET  •  SISTEMA DE GESTIÓN Y VENTAS",
            font=("Segoe UI", 12, "bold"),
            fg="#FFFFFF",
            bg="#8FA4B5"
        )
        lbl_logo.pack(side="left")

        # Contenedor de usuario y control de sesión
        user_panel = tk.Frame(header_frame, bg="#8FA4B5")
        user_panel.pack(side="right", padx=15, pady=8)

        lbl_usuario = tk.Label(
            user_panel,
            text=f"👤 Conectado: {self.usuario_autenticado.nombre}",
            font=("Segoe UI", 9, "bold"),
            fg="#F8FAFC",
            bg="#8FA4B5"
        )
        lbl_usuario.pack(side="left", padx=(0, 14))

        btn_salir = tk.Button(
            user_panel,
            text="🚪 Cerrar Sesión",
            font=("Segoe UI", 8, "bold"),
            bg="#FECDD3",              # Rosa pastel
            fg="#881337",              # Rojo borgoña suave
            activebackground="#FDA4AF",
            activeforeground="#881337",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=3,
            command=self._confirmar_cierre_sesion
        )
        btn_salir.pack(side="left")

        # ---------------------------------------------------------------------
        # 2. CONTENEDOR CENTRAL: Notebook con pestañas de navegación
        # ---------------------------------------------------------------------
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=(8, 4))

        self.tab_productos = ttk.Frame(self.notebook, padding=10)
        self.tab_usuarios = ttk.Frame(self.notebook, padding=10)
        self.tab_ventas = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.tab_productos, text="  🍲 Gestión de Productos  ")
        self.notebook.add(self.tab_usuarios, text="  👥 Consulta de Usuarios  ")
        self.notebook.add(self.tab_ventas, text="  🧾 Registro y Gestión de Ventas  ")

        self._construir_pestana_productos()
        self._construir_pestana_usuarios()
        self._construir_pestana_ventas()

        # ---------------------------------------------------------------------
        # 3. CONTENEDOR INFERIOR: Barra de estado
        # ---------------------------------------------------------------------
        status_bar = tk.Frame(self, bg="#E2E8F0", height=24)
        status_bar.pack(fill="x", side="bottom")

        lbl_status = tk.Label(
            status_bar,
            text="Semana 15 • POO UEA — Manejo de Eventos, Callbacks y Transacciones de Ventas",
            font=("Segoe UI", 8),
            fg="#475569",
            bg="#E2E8F0",
            padx=12,
            pady=2
        )
        lbl_status.pack(side="left")

    # =========================================================================
    # PESTAÑA 1: GESTIÓN DE PRODUCTOS (CRUD Y CATÁLOGO)
    # =========================================================================

    def _construir_pestana_productos(self) -> None:
        """Construye la sección de productos con métricas, formulario y catálogo."""
        # --- ZONA A: Tarjetas Métricas Superiores (Colores pasteles) ---
        metricas_frame = tk.Frame(self.tab_productos, bg="#F1F5F9")
        metricas_frame.pack(fill="x", pady=(0, 8))

        # Tarjeta 1: Total Productos (Lavanda pastel)
        c1 = tk.Frame(metricas_frame, bg="#EDE9FE", bd=1, relief="solid")
        c1.pack(side="left", fill="both", expand=True, padx=4, pady=2)
        tk.Label(c1, text="📦 TOTAL PRODUCTOS", font=("Segoe UI", 8, "bold"), bg="#EDE9FE", fg="#5B21B6").pack(anchor="w", padx=8, pady=(4, 0))
        self.lbl_metrica_total = tk.Label(c1, text="0", font=("Segoe UI", 13, "bold"), bg="#EDE9FE", fg="#4C1D95")
        self.lbl_metrica_total.pack(anchor="w", padx=8, pady=(0, 4))

        # Tarjeta 2: Stock Acumulado (Menta pastel)
        c2 = tk.Frame(metricas_frame, bg="#DCFCE7", bd=1, relief="solid")
        c2.pack(side="left", fill="both", expand=True, padx=4, pady=2)
        tk.Label(c2, text="📊 STOCK ACUMULADO", font=("Segoe UI", 8, "bold"), bg="#DCFCE7", fg="#166534").pack(anchor="w", padx=8, pady=(4, 0))
        self.lbl_metrica_stock = tk.Label(c2, text="0 uds", font=("Segoe UI", 13, "bold"), bg="#DCFCE7", fg="#14532D")
        self.lbl_metrica_stock.pack(anchor="w", padx=8, pady=(0, 4))

        # Tarjeta 3: Categorías Activas (Ámbar pastel)
        c3 = tk.Frame(metricas_frame, bg="#FEF3C7", bd=1, relief="solid")
        c3.pack(side="left", fill="both", expand=True, padx=4, pady=2)
        tk.Label(c3, text="🏷️ CATEGORÍAS DISPONIBLES", font=("Segoe UI", 8, "bold"), bg="#FEF3C7", fg="#92400E").pack(anchor="w", padx=8, pady=(4, 0))
        self.lbl_metrica_cat = tk.Label(c3, text="0 categorías", font=("Segoe UI", 13, "bold"), bg="#FEF3C7", fg="#78350F")
        self.lbl_metrica_cat.pack(anchor="w", padx=8, pady=(0, 4))

        # --- ZONA B: Formulario de Entrada (LabelFrame con Grid) ---
        self.form_frame = ttk.LabelFrame(
            self.tab_productos,
            text=" 📋 Formulario de Producto (Registro / Consulta / Edición) ",
            padding=(12, 8)
        )
        self.form_frame.pack(fill="x", pady=(0, 8))

        for col_idx in range(6):
            self.form_frame.columnconfigure(col_idx, weight=1)

        # Fila 0: Código, Nombre y Categoría
        lbl_codigo = ttk.Label(self.form_frame, text="Código:", font=("Segoe UI", 9, "bold"))
        lbl_codigo.grid(row=0, column=0, sticky="w", padx=4, pady=3)
        self.txt_codigo = ttk.Entry(self.form_frame, width=12, font=("Segoe UI", 9))
        self.txt_codigo.grid(row=0, column=1, sticky="ew", padx=4, pady=3)

        lbl_nombre = ttk.Label(self.form_frame, text="Nombre:", font=("Segoe UI", 9, "bold"))
        lbl_nombre.grid(row=0, column=2, sticky="w", padx=4, pady=3)
        self.txt_nombre = ttk.Entry(self.form_frame, width=24, font=("Segoe UI", 9))
        self.txt_nombre.grid(row=0, column=3, sticky="ew", padx=4, pady=3)

        lbl_categoria = ttk.Label(self.form_frame, text="Categoría:", font=("Segoe UI", 9, "bold"))
        lbl_categoria.grid(row=0, column=4, sticky="w", padx=4, pady=3)
        self.cmb_categoria = ttk.Combobox(
            self.form_frame,
            values=["Carnes", "Mariscos", "Bebidas", "Postres", "Entradas", "Pastas", "Ensaladas"],
            font=("Segoe UI", 9),
            width=16
        )
        self.cmb_categoria.grid(row=0, column=5, sticky="ew", padx=4, pady=3)
        self.cmb_categoria.set("Carnes")

        # Fila 1: Precio y Stock
        lbl_precio = ttk.Label(self.form_frame, text="Precio ($):", font=("Segoe UI", 9, "bold"))
        lbl_precio.grid(row=1, column=0, sticky="w", padx=4, pady=3)
        self.txt_precio = ttk.Entry(self.form_frame, width=12, font=("Segoe UI", 9))
        self.txt_precio.grid(row=1, column=1, sticky="ew", padx=4, pady=3)

        lbl_stock = ttk.Label(self.form_frame, text="Stock (uds):", font=("Segoe UI", 9, "bold"))
        lbl_stock.grid(row=1, column=2, sticky="w", padx=4, pady=3)
        self.txt_stock = ttk.Entry(self.form_frame, width=12, font=("Segoe UI", 9))
        self.txt_stock.grid(row=1, column=3, sticky="ew", padx=4, pady=3)

        lbl_pista = ttk.Label(
            self.form_frame,
            text="💡 Ingrese el Código y use 'Cargar' para consultar, o complete todos los campos para 'Registrar'.",
            font=("Segoe UI", 8, "italic"),
            foreground="#64748B"
        )
        lbl_pista.grid(row=1, column=4, columnspan=2, sticky="w", padx=4, pady=3)

        # --- ZONA C: Contenedor de Botonera de Acciones (Colores Pasteles) ---
        acciones_frame = tk.Frame(self.tab_productos, bg="#F8FAFC", pady=4)
        acciones_frame.pack(fill="x", pady=(0, 6))

        # Botón 1: REGISTRAR (Pastel Menta)
        self.btn_registrar = tk.Button(
            acciones_frame,
            text="➕ Registrar",
            font=("Segoe UI", 9, "bold"),
            bg="#A7F3D0",
            fg="#065F46",
            activebackground="#6EE7B7",
            activeforeground="#064E3B",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=4,
            command=self._registrar_producto
        )
        self.btn_registrar.pack(side="left", padx=4)

        # Botón 2: CARGAR / CONSULTAR (Pastel Celeste)
        self.btn_consultar = tk.Button(
            acciones_frame,
            text="🔍 Cargar / Consultar",
            font=("Segoe UI", 9, "bold"),
            bg="#BAE6FD",
            fg="#075985",
            activebackground="#7DD3FC",
            activeforeground="#0C4A6E",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=4,
            command=self._cargar_o_consultar_producto
        )
        self.btn_consultar.pack(side="left", padx=4)

        # Botón 3: ACTUALIZAR (Pastel Durazno)
        self.btn_actualizar = tk.Button(
            acciones_frame,
            text="✏️ Actualizar",
            font=("Segoe UI", 9, "bold"),
            bg="#FED7AA",
            fg="#9A3412",
            activebackground="#FDBA74",
            activeforeground="#7C2D12",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=4,
            command=self._actualizar_producto
        )
        self.btn_actualizar.pack(side="left", padx=4)

        # Botón 4: ELIMINAR (Pastel Rosa)
        self.btn_eliminar = tk.Button(
            acciones_frame,
            text="🗑️ Eliminar",
            font=("Segoe UI", 9, "bold"),
            bg="#FECDD3",
            fg="#9F1239",
            activebackground="#FDA4AF",
            activeforeground="#881337",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=4,
            command=self._eliminar_producto
        )
        self.btn_eliminar.pack(side="left", padx=4)

        # Botón 5: LIMPIAR (Pastel Gris)
        self.btn_limpiar = tk.Button(
            acciones_frame,
            text="🧹 Limpiar Campos",
            font=("Segoe UI", 9),
            bg="#E2E8F0",
            fg="#334155",
            activebackground="#CBD5E1",
            activeforeground="#1E293B",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=self._limpiar_formulario
        )
        self.btn_limpiar.pack(side="left", padx=4)

        # Botón 6: CARGAR SELECCIONADO DE TABLA (Pastel Lavanda)
        self.btn_cargar_sel = tk.Button(
            acciones_frame,
            text="📋 Cargar Seleccionado de Tabla",
            font=("Segoe UI", 9),
            bg="#E9D5FF",
            fg="#581C87",
            activebackground="#D8B4FE",
            activeforeground="#3B0764",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=self._cargar_seleccionado_de_tabla
        )
        self.btn_cargar_sel.pack(side="right", padx=4)

        # --- BANNER DE ESTADO Y FEEDBACK VISUAL ---
        self.banner_estado = tk.Frame(self.tab_productos, bg="#F1F5F9", bd=1, relief="groove")
        self.banner_estado.pack(fill="x", pady=(0, 6))

        self.lbl_estado_producto = tk.Label(
            self.banner_estado,
            text="Listo. Seleccione un producto o ingrese datos en el formulario.",
            font=("Segoe UI", 9),
            fg="#334155",
            bg="#F1F5F9",
            padx=8,
            pady=3
        )
        self.lbl_estado_producto.pack(side="left")

        # --- ZONA D: Contenedor de Tabla y Catálogo (Treeview + Scrollbar) ---
        catalogo_frame = ttk.LabelFrame(
            self.tab_productos,
            text=" 📦 Catálogo de Productos Registrados (Persistencia en productos.json) ",
            padding=(8, 6)
        )
        catalogo_frame.pack(fill="both", expand=True)

        columnas = ("codigo", "nombre", "categoria", "precio", "stock")
        self.tree_productos = ttk.Treeview(
            catalogo_frame,
            columns=columnas,
            show="headings",
            selectmode="browse",
            height=8
        )

        self.tree_productos.heading("codigo", text="Código")
        self.tree_productos.heading("nombre", text="Nombre del Producto")
        self.tree_productos.heading("categoria", text="Categoría")
        self.tree_productos.heading("precio", text="Precio Unitario ($)")
        self.tree_productos.heading("stock", text="Stock (uds)")

        self.tree_productos.column("codigo", width=85, anchor="center")
        self.tree_productos.column("nombre", width=240, anchor="w")
        self.tree_productos.column("categoria", width=140, anchor="center")
        self.tree_productos.column("precio", width=110, anchor="e")
        self.tree_productos.column("stock", width=95, anchor="center")

        self.tree_productos.tag_configure("fila_par", background="#FFFFFF")
        self.tree_productos.tag_configure("fila_impar", background="#F8FAFC")

        scrollbar_prod = ttk.Scrollbar(
            catalogo_frame,
            orient="vertical",
            command=self.tree_productos.yview
        )
        self.tree_productos.configure(yscrollcommand=scrollbar_prod.set)

        self.tree_productos.pack(side="left", fill="both", expand=True)
        scrollbar_prod.pack(side="right", fill="y")

    # =========================================================================
    # PESTAÑA 2: CONSULTA DE USUARIOS REGISTRADOS
    # =========================================================================

    def _construir_pestana_usuarios(self) -> None:
        """Construye la vista organizada para consultar los usuarios del sistema."""
        top_bar = tk.Frame(self.tab_usuarios, bg="#F1F5F9", pady=6)
        top_bar.pack(fill="x", pady=(0, 8))

        # Tarjeta métrica de usuarios
        card_usr = tk.Frame(top_bar, bg="#E0F2FE", bd=1, relief="solid")
        card_usr.pack(side="left", padx=4)
        tk.Label(card_usr, text="👥 TOTAL USUARIOS REGISTRADOS", font=("Segoe UI", 8, "bold"), bg="#E0F2FE", fg="#0369A1").pack(anchor="w", padx=10, pady=(4, 0))
        self.lbl_metrica_usuarios = tk.Label(card_usr, text="0 usuarios", font=("Segoe UI", 12, "bold"), bg="#E0F2FE", fg="#075985")
        self.lbl_metrica_usuarios.pack(anchor="w", padx=10, pady=(0, 4))

        btn_recargar_usr = tk.Button(
            top_bar,
            text="🔄 Actualizar Lista",
            font=("Segoe UI", 8),
            bg="#E2E8F0",
            fg="#334155",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=4,
            command=self.cargar_usuarios
        )
        btn_recargar_usr.pack(side="right", padx=6)

        # Contenedor de la tabla de usuarios
        frame_tabla_usr = ttk.LabelFrame(self.tab_usuarios, text=" 👥 Usuarios y Credenciales del Sistema ", padding=8)
        frame_tabla_usr.pack(fill="both", expand=True)

        columnas = ("identificacion", "nombre", "correo")
        self.tree_usuarios = ttk.Treeview(
            frame_tabla_usr,
            columns=columnas,
            show="headings",
            selectmode="browse",
            height=12
        )

        self.tree_usuarios.heading("identificacion", text="Identificación / Cédula")
        self.tree_usuarios.heading("nombre", text="Nombre Completo")
        self.tree_usuarios.heading("correo", text="Correo Electrónico")

        self.tree_usuarios.column("identificacion", width=160, anchor="center")
        self.tree_usuarios.column("nombre", width=250, anchor="w")
        self.tree_usuarios.column("correo", width=270, anchor="w")

        self.tree_usuarios.tag_configure("fila_par", background="#FFFFFF")
        self.tree_usuarios.tag_configure("fila_impar", background="#F8FAFC")

        scrollbar_usr = ttk.Scrollbar(
            frame_tabla_usr,
            orient="vertical",
            command=self.tree_usuarios.yview
        )
        self.tree_usuarios.configure(yscrollcommand=scrollbar_usr.set)

        self.tree_usuarios.pack(side="left", fill="both", expand=True)
        scrollbar_usr.pack(side="right", fill="y")

    # =========================================================================
    # PESTAÑA 3: REGISTRO Y GESTIÓN DE VENTAS (SEMANA 15 - MANEJO DE EVENTOS)
    # =========================================================================

    def _construir_pestana_ventas(self) -> None:
        """
        Construye la sección de Ventas demostrando el fundamento de eventos:
        USUARIO -> ACCIÓN -> BOTÓN con command= -> CALLBACK -> SERVICIO -> PERSISTENCIA -> RESPUESTA.
        """
        # --- ZONA A: Tarjetas Métricas Superiores de Ventas (Tonos pasteles) ---
        metricas_ventas_frame = tk.Frame(self.tab_ventas, bg="#F1F5F9")
        metricas_ventas_frame.pack(fill="x", pady=(0, 8))

        # Tarjeta 1: Total Ventas Realizadas (Lavanda pastel)
        v1 = tk.Frame(metricas_ventas_frame, bg="#EDE9FE", bd=1, relief="solid")
        v1.pack(side="left", fill="both", expand=True, padx=4, pady=2)
        tk.Label(v1, text="🧾 VENTAS REALIZADAS", font=("Segoe UI", 8, "bold"), bg="#EDE9FE", fg="#5B21B6").pack(anchor="w", padx=8, pady=(4, 0))
        self.lbl_metrica_ventas_cant = tk.Label(v1, text="0 ventas", font=("Segoe UI", 13, "bold"), bg="#EDE9FE", fg="#4C1D95")
        self.lbl_metrica_ventas_cant.pack(anchor="w", padx=8, pady=(0, 4))

        # Tarjeta 2: Ingresos Totales Acumulados (Menta pastel)
        v2 = tk.Frame(metricas_ventas_frame, bg="#DCFCE7", bd=1, relief="solid")
        v2.pack(side="left", fill="both", expand=True, padx=4, pady=2)
        tk.Label(v2, text="💰 INGRESOS TOTALES", font=("Segoe UI", 8, "bold"), bg="#DCFCE7", fg="#166534").pack(anchor="w", padx=8, pady=(4, 0))
        self.lbl_metrica_ventas_ingresos = tk.Label(v2, text="$0.00", font=("Segoe UI", 13, "bold"), bg="#DCFCE7", fg="#14532D")
        self.lbl_metrica_ventas_ingresos.pack(anchor="w", padx=8, pady=(0, 4))

        # Tarjeta 3: Unidades Despachadas (Ámbar pastel)
        v3 = tk.Frame(metricas_ventas_frame, bg="#FEF3C7", bd=1, relief="solid")
        v3.pack(side="left", fill="both", expand=True, padx=4, pady=2)
        tk.Label(v3, text="📦 PLATOS DESPACHADOS", font=("Segoe UI", 8, "bold"), bg="#FEF3C7", fg="#92400E").pack(anchor="w", padx=8, pady=(4, 0))
        self.lbl_metrica_ventas_unidades = tk.Label(v3, text="0 uds", font=("Segoe UI", 13, "bold"), bg="#FEF3C7", fg="#78350F")
        self.lbl_metrica_ventas_unidades.pack(anchor="w", padx=8, pady=(0, 4))

        # --- ZONA B: Formulario de Registro de Venta (LabelFrame con Grid) ---
        self.form_venta_frame = ttk.LabelFrame(
            self.tab_ventas,
            text=" 🛒 Nueva Venta: Selección de Usuario y Producto ",
            padding=(12, 8)
        )
        self.form_venta_frame.pack(fill="x", pady=(0, 8))

        self.form_venta_frame.columnconfigure(0, weight=0)
        self.form_venta_frame.columnconfigure(1, weight=1)
        self.form_venta_frame.columnconfigure(2, weight=0)
        self.form_venta_frame.columnconfigure(3, weight=1)

        # Fila 0: Selección de Usuario y Producto
        lbl_usr_vta = ttk.Label(self.form_venta_frame, text="Cliente / Usuario:", font=("Segoe UI", 9, "bold"))
        lbl_usr_vta.grid(row=0, column=0, sticky="w", padx=4, pady=4)

        self.cmb_venta_usuario = ttk.Combobox(self.form_venta_frame, state="readonly", font=("Segoe UI", 9))
        self.cmb_venta_usuario.grid(row=0, column=1, sticky="ew", padx=4, pady=4)

        lbl_prd_vta = ttk.Label(self.form_venta_frame, text="Producto a Vender:", font=("Segoe UI", 9, "bold"))
        lbl_prd_vta.grid(row=0, column=2, sticky="w", padx=8, pady=4)

        self.cmb_venta_producto = ttk.Combobox(self.form_venta_frame, state="readonly", font=("Segoe UI", 9))
        self.cmb_venta_producto.grid(row=0, column=3, sticky="ew", padx=4, pady=4)
        self.cmb_venta_producto.bind("<<ComboboxSelected>>", self._al_cambiar_seleccion_producto)

        # Fila 1: Cantidad, Detalle de Stock y Total Estimado en Vivo
        lbl_cant_vta = ttk.Label(self.form_venta_frame, text="Cantidad:", font=("Segoe UI", 9, "bold"))
        lbl_cant_vta.grid(row=1, column=0, sticky="w", padx=4, pady=4)

        cant_box = ttk.Frame(self.form_venta_frame)
        cant_box.grid(row=1, column=1, sticky="w", padx=4, pady=4)

        self.spn_venta_cantidad = ttk.Spinbox(
            cant_box,
            from_=1,
            to=999,
            width=6,
            font=("Segoe UI", 9),
            command=self._actualizar_calculo_venta
        )
        self.spn_venta_cantidad.pack(side="left")
        self.spn_venta_cantidad.set(1)
        self.spn_venta_cantidad.bind("<KeyRelease>", self._actualizar_calculo_venta)

        self.lbl_stock_disponible = ttk.Label(
            cant_box,
            text="  (Disponible: -- uds)",
            font=("Segoe UI", 8, "italic"),
            foreground="#64748B"
        )
        self.lbl_stock_disponible.pack(side="left", padx=4)

        # Total a pagar en vivo
        lbl_calc_titulo = ttk.Label(self.form_venta_frame, text="Total Estimado:", font=("Segoe UI", 9, "bold"))
        lbl_calc_titulo.grid(row=1, column=2, sticky="w", padx=8, pady=4)

        self.lbl_venta_total_estimado = ttk.Label(
            self.form_venta_frame,
            text="$0.00",
            font=("Segoe UI", 11, "bold"),
            foreground="#065F46"
        )
        self.lbl_venta_total_estimado.grid(row=1, column=3, sticky="w", padx=4, pady=4)

        # --- ZONA C: Botonera de Acciones (Demostración de command= y Callback) ---
        acciones_vta_frame = tk.Frame(self.tab_ventas, bg="#F8FAFC", pady=4)
        acciones_vta_frame.pack(fill="x", pady=(0, 6))

        # BOTÓN PRINCIPAL: REGISTRAR VENTA (Vinculado mediante command= al Callback)
        self.btn_registrar_venta = tk.Button(
            acciones_vta_frame,
            text="🛒  Registrar Venta",
            font=("Segoe UI", 9, "bold"),
            bg="#A7F3D0",              # Verde menta pastel
            fg="#065F46",              # Verde oscuro legible
            activebackground="#6EE7B7",
            activeforeground="#064E3B",
            relief="flat",
            cursor="hand2",
            padx=14,
            pady=5,
            command=self._callback_registrar_venta  # FUNDAMENTO: command= enlaza el callback
        )
        self.btn_registrar_venta.pack(side="left", padx=4)

        # Botón secundario: Limpiar formulario de venta
        self.btn_limpiar_venta = tk.Button(
            acciones_vta_frame,
            text="🧹 Limpiar Formulario",
            font=("Segoe UI", 9),
            bg="#E2E8F0",              # Gris pastel
            fg="#334155",
            activebackground="#CBD5E1",
            activeforeground="#1E293B",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=5,
            command=self._limpiar_formulario_venta
        )
        self.btn_limpiar_venta.pack(side="left", padx=4)

        # Botón de consulta de detalle
        self.btn_ver_detalle_venta = tk.Button(
            acciones_vta_frame,
            text="🔍 Ver Detalle de Transacción",
            font=("Segoe UI", 9),
            bg="#BAE6FD",              # Celeste pastel
            fg="#075985",
            activebackground="#7DD3FC",
            activeforeground="#0C4A6E",
            relief="flat",
            cursor="hand2",
            padx=10,
            pady=5,
            command=self._consultar_detalle_venta_seleccionada
        )
        self.btn_ver_detalle_venta.pack(side="right", padx=4)

        # --- ZONA D: Banner de Estado y Feedback Visual de Ventas ---
        self.banner_estado_ventas = tk.Frame(self.tab_ventas, bg="#F1F5F9", bd=1, relief="groove")
        self.banner_estado_ventas.pack(fill="x", pady=(0, 6))

        self.lbl_estado_ventas = tk.Label(
            self.banner_estado_ventas,
            text="Listo para registrar operaciones. Seleccione un cliente y un producto.",
            font=("Segoe UI", 9),
            fg="#334155",
            bg="#F1F5F9",
            padx=8,
            pady=3
        )
        self.lbl_estado_ventas.pack(side="left")

        # --- ZONA E: Tabla de Ventas Registradas (Treeview + Scrollbar) ---
        historial_frame = ttk.LabelFrame(
            self.tab_ventas,
            text=" 📜 Historial de Ventas Registradas (Persistencia en ventas.json) ",
            padding=(8, 6)
        )
        historial_frame.pack(fill="both", expand=True)

        columnas_vta = ("id_venta", "fecha", "usuario", "producto", "precio", "cantidad", "total")
        self.tree_ventas = ttk.Treeview(
            historial_frame,
            columns=columnas_vta,
            show="headings",
            selectmode="browse",
            height=8
        )

        self.tree_ventas.heading("id_venta", text="ID Venta")
        self.tree_ventas.heading("fecha", text="Fecha y Hora")
        self.tree_ventas.heading("usuario", text="Cliente / Usuario")
        self.tree_ventas.heading("producto", text="Producto Vendido")
        self.tree_ventas.heading("precio", text="Precio Unit.")
        self.tree_ventas.heading("cantidad", text="Cant.")
        self.tree_ventas.heading("total", text="Total ($)")

        self.tree_ventas.column("id_venta", width=80, anchor="center")
        self.tree_ventas.column("fecha", width=140, anchor="center")
        self.tree_ventas.column("usuario", width=160, anchor="w")
        self.tree_ventas.column("producto", width=190, anchor="w")
        self.tree_ventas.column("precio", width=90, anchor="e")
        self.tree_ventas.column("cantidad", width=60, anchor="center")
        self.tree_ventas.column("total", width=95, anchor="e")

        self.tree_ventas.tag_configure("fila_par", background="#FFFFFF")
        self.tree_ventas.tag_configure("fila_impar", background="#F8FAFC")

        scrollbar_vta = ttk.Scrollbar(
            historial_frame,
            orient="vertical",
            command=self.tree_ventas.yview
        )
        self.tree_ventas.configure(yscrollcommand=scrollbar_vta.set)

        self.tree_ventas.pack(side="left", fill="both", expand=True)
        scrollbar_vta.pack(side="right", fill="y")

    # =========================================================================
    # MANEJO DE EVENTOS Y CALLBACKS DEL MÓDULO DE VENTAS
    # =========================================================================

    def _callback_registrar_venta(self) -> None:
        """
        CALLBACK DE VENTA (Semana 15):
        Flujo de ejecución riguroso:
        1. USUARIO realiza la acción pulsando 'Registrar Venta'.
        2. BOTÓN activa command=_callback_registrar_venta.
        3. CALLBACK extrae los datos de la interfaz gráfica.
        4. CALLBACK delega la validación, descuento de stock y persistencia a RestauranteServicio.
        5. PERSISTENCIA se completa en ventas.json y productos.json.
        6. RESPUESTA VISUAL actualiza Treeviews (ventas y productos), métricas, comboboxes y alerta.
        """
        # 1. Obtener selecciones de la UI
        texto_usuario = self.cmb_venta_usuario.get().strip()
        texto_producto = self.cmb_venta_producto.get().strip()
        texto_cantidad = self.spn_venta_cantidad.get().strip()

        # Validación visual inicial
        if not texto_usuario:
            self._mostrar_estado_ventas("⚠️ Debe seleccionar un usuario/cliente de la lista.", "advertencia")
            self.cmb_venta_usuario.focus_set()
            return

        if not texto_producto:
            self._mostrar_estado_ventas("⚠️ Debe seleccionar un producto del catálogo para vender.", "advertencia")
            self.cmb_venta_producto.focus_set()
            return

        # 2. Extraer claves de dominio a partir de los mapeos
        id_usuario = self._mapa_usuarios_combo.get(texto_usuario)
        codigo_producto = self._mapa_productos_combo.get(texto_producto)

        if not id_usuario or not codigo_producto:
            self._mostrar_estado_ventas("⚠️ Error al identificar el usuario o producto seleccionado.", "error")
            return

        # Validar formato de cantidad
        try:
            cant_val = int(texto_cantidad)
            if cant_val < 1:
                raise ValueError()
        except ValueError:
            self._mostrar_estado_ventas("⚠️ La cantidad debe ser un número entero mayor o igual a 1.", "advertencia")
            self.spn_venta_cantidad.focus_set()
            return

        # 3. Delegación de la operación a la Capa de Servicios
        try:
            nueva_venta = self.restaurante_servicio.registrar_venta(
                id_usuario=id_usuario,
                codigo_producto=codigo_producto,
                cantidad=cant_val
            )

            # 4. Respuesta Visual Inmediata: Actualización integral del sistema
            self.cargar_ventas()
            self._actualizar_metricas_ventas()

            # Reflejar el stock descontado en la pestaña de productos
            self.cargar_productos()
            self._actualizar_metricas()

            # Refrescar los textos de los combos para mostrar el stock actualizado
            self._cargar_opciones_combobox_ventas()

            # Mensaje en banner
            msg_exito = (
                f"✅ ¡Venta '{nueva_venta.id_venta}' registrada! "
                f"{nueva_venta.nombre_producto} x{nueva_venta.cantidad} | Total: ${nueva_venta.total:.2f}"
            )
            self._mostrar_estado_ventas(msg_exito, "exito")

            # Cuadro de diálogo de confirmación
            prod_actualizado = self.restaurante_servicio.buscar_producto(codigo_producto)
            stock_restante = prod_actualizado.stock if prod_actualizado else 0

            detalle_dialogo = (
                f"Transacción [{nueva_venta.id_venta}] registrada exitosamente.\n\n"
                f"• Cliente: {nueva_venta.nombre_usuario}\n"
                f"• Producto: {nueva_venta.nombre_producto}\n"
                f"• Cantidad vendida: {nueva_venta.cantidad} unidad(es)\n"
                f"• Precio unitario: ${nueva_venta.precio_unitario:.2f}\n"
                f"• Total cobrado: ${nueva_venta.total:.2f}\n"
                f"• Stock restante en inventario: {stock_restante} unidades\n\n"
                f"Persistencia garantizada en ventas.json y productos.json."
            )
            messagebox.showinfo("Venta Exitosa", detalle_dialogo, parent=self)

            # Restablecer el formulario
            self._limpiar_formulario_venta(mantener_estado=True)

        except ValueError as e:
            # Reglas de negocio incumplidas (ej. stock insuficiente, usuario no válido)
            self._mostrar_estado_ventas(f"❌ Validación de venta: {e}", "advertencia")
            messagebox.showwarning("Aviso de Negocio", str(e), parent=self)
        except Exception as e:
            # Errores del sistema de persistencia o E/S
            self._mostrar_estado_ventas(f"❌ Error al registrar venta: {e}", "error")
            messagebox.showerror("Error en Transacción", str(e), parent=self)

    def _al_cambiar_seleccion_producto(self, event=None) -> None:
        """Callback al seleccionar un producto en el combobox para calcular precio y stock."""
        texto_producto = self.cmb_venta_producto.get().strip()
        codigo_producto = self._mapa_productos_combo.get(texto_producto)
        
        if codigo_producto:
            producto = self.restaurante_servicio.buscar_producto(codigo_producto)
            if producto:
                self.lbl_stock_disponible.config(text=f"  (Disponible: {producto.stock} uds)")
        
        self._actualizar_calculo_venta()

    def _actualizar_calculo_venta(self, event=None) -> None:
        """Calcula dinámicamente el total estimado en pantalla según el producto y cantidad."""
        texto_producto = self.cmb_venta_producto.get().strip()
        codigo_producto = self._mapa_productos_combo.get(texto_producto)

        if not codigo_producto:
            self.lbl_venta_total_estimado.config(text="$0.00")
            return

        producto = self.restaurante_servicio.buscar_producto(codigo_producto)
        if not producto:
            self.lbl_venta_total_estimado.config(text="$0.00")
            return

        try:
            cant = int(self.spn_venta_cantidad.get())
            if cant <= 0:
                cant = 1
        except (ValueError, TypeError):
            cant = 1

        total = round(producto.precio * cant, 2)
        self.lbl_venta_total_estimado.config(text=f"${total:.2f}")

    def _limpiar_formulario_venta(self, mantener_estado: bool = False) -> None:
        """Restablece los campos de selección del formulario de venta."""
        if self.cmb_venta_usuario["values"]:
            self.cmb_venta_usuario.current(0)
        else:
            self.cmb_venta_usuario.set("")

        if self.cmb_venta_producto["values"]:
            self.cmb_venta_producto.current(0)
        else:
            self.cmb_venta_producto.set("")

        self.spn_venta_cantidad.set(1)
        self._al_cambiar_seleccion_producto()

        if not mantener_estado:
            self._mostrar_estado_ventas("Formulario de venta listo para una nueva orden.", "info")

    def _consultar_detalle_venta_seleccionada(self) -> None:
        """Muestra el detalle completo de la venta seleccionada en la tabla."""
        seleccion = self.tree_ventas.selection()
        if not seleccion:
            self._mostrar_estado_ventas("⚠️ Seleccione una venta del historial para ver su detalle.", "advertencia")
            return

        item = self.tree_ventas.item(seleccion[0])
        valores = item.get("values", [])
        if not valores:
            return

        id_venta = str(valores[0])
        venta = self.restaurante_servicio.buscar_venta(id_venta)
        if venta:
            info = (
                f"🧾 DETALLE DE LA TRANSACCIÓN: {venta.id_venta}\n"
                f"─────────────────────────────────────\n"
                f"• Fecha y Hora: {venta.fecha}\n"
                f"• Cliente / Usuario: {venta.nombre_usuario} [{venta.id_usuario}]\n"
                f"• Producto: {venta.nombre_producto} [{venta.codigo_producto}]\n"
                f"• Precio Unitario: ${venta.precio_unitario:.2f}\n"
                f"• Cantidad: {venta.cantidad} unidad(es)\n"
                f"• Importe Total: ${venta.total:.2f}\n"
                f"─────────────────────────────────────\n"
                f"Estado: Confirmada y Guardada en ventas.json"
            )
            messagebox.showinfo(f"Detalle de Venta [{venta.id_venta}]", info, parent=self)
            self._mostrar_estado_ventas(f"🔍 Inspeccionando detalle de venta [{venta.id_venta}].", "info")

    def _mostrar_estado_ventas(self, mensaje: str, tipo: str = "info") -> None:
        """Actualiza el banner de retroalimentación de la pestaña de ventas."""
        configuraciones = {
            "exito": {"bg": "#DCFCE7", "fg": "#14532D"},
            "error": {"bg": "#FEE2E2", "fg": "#991B1B"},
            "advertencia": {"bg": "#FEF3C7", "fg": "#92400E"},
            "info": {"bg": "#F1F5F9", "fg": "#334155"}
        }
        cfg = configuraciones.get(tipo, {"bg": "#F1F5F9", "fg": "#334155"})
        self.banner_estado_ventas.config(bg=cfg["bg"])
        self.lbl_estado_ventas.config(text=mensaje, bg=cfg["bg"], fg=cfg["fg"])

    # =========================================================================
    # OPERACIONES CRUD SOBRE PRODUCTOS (DELEGADAS A RESTAURANTESERVICIO)
    # =========================================================================

    def _obtener_datos_formulario(self) -> dict:
        """Recupera los valores de los campos del formulario de producto."""
        return {
            "codigo": self.txt_codigo.get().strip(),
            "nombre": self.txt_nombre.get().strip(),
            "categoria": self.cmb_categoria.get().strip(),
            "precio": self.txt_precio.get().strip(),
            "stock": self.txt_stock.get().strip()
        }

    def _registrar_producto(self) -> None:
        """Acción del botón 'Registrar' en Productos."""
        datos = self._obtener_datos_formulario()

        if not datos["codigo"] or not datos["nombre"] or not datos["precio"] or not datos["stock"]:
            self._mostrar_estado("⚠️ Todos los campos son obligatorios para registrar un producto.", "advertencia")
            return

        try:
            precio_val = float(datos["precio"])
            stock_val = int(datos["stock"])
        except ValueError:
            self._mostrar_estado("⚠️ El precio debe ser un número decimal y el stock un número entero.", "advertencia")
            return

        try:
            nuevo_prod = self.restaurante_servicio.registrar_producto(
                codigo=datos["codigo"],
                nombre=datos["nombre"],
                categoria=datos["categoria"],
                precio=precio_val,
                stock=stock_val
            )
            self.cargar_productos()
            self._actualizar_metricas()
            self._cargar_opciones_combobox_ventas()
            self._mostrar_estado(f"✅ ¡Producto '{nuevo_prod.nombre}' [{nuevo_prod.codigo}] registrado con éxito!", "exito")
            messagebox.showinfo(
                "Registro Exitoso",
                f"El producto '{nuevo_prod.nombre}' [{nuevo_prod.codigo}] fue guardado en productos.json.",
                parent=self
            )
            self._limpiar_formulario(mantener_estado=True)
        except ValueError as e:
            self._mostrar_estado(f"❌ Error de validación: {e}", "error")
            messagebox.showwarning("Aviso de Validación", str(e), parent=self)
        except Exception as e:
            self._mostrar_estado(f"❌ Error al registrar: {e}", "error")
            messagebox.showerror("Error", str(e), parent=self)

    def _cargar_o_consultar_producto(self) -> None:
        """Acción del botón 'Cargar / Consultar' en Productos."""
        codigo = self.txt_codigo.get().strip()
        if not codigo:
            self._mostrar_estado("⚠️ Ingrese el código del producto a consultar.", "advertencia")
            self.txt_codigo.focus_set()
            return

        producto = self.restaurante_servicio.buscar_producto(codigo)
        if producto is None:
            self._mostrar_estado(f"❌ No se encontró ningún producto con el código '{codigo.upper()}'.", "error")
            messagebox.showinfo("Búsqueda", f"No existe un producto con código '{codigo.upper()}'.", parent=self)
            return

        self._llenar_formulario(producto)
        self._mostrar_estado(f"🔍 Producto '{producto.nombre}' [{producto.codigo}] cargado.", "info")

    def _actualizar_producto(self) -> None:
        """Acción del botón 'Actualizar' en Productos."""
        datos = self._obtener_datos_formulario()

        if not datos["codigo"]:
            self._mostrar_estado("⚠️ Ingrese el código del producto que desea actualizar.", "advertencia")
            self.txt_codigo.focus_set()
            return

        try:
            precio_val = float(datos["precio"])
            stock_val = int(datos["stock"])
        except ValueError:
            self._mostrar_estado("⚠️ El precio debe ser un número decimal y el stock un número entero.", "advertencia")
            return

        try:
            producto_act = self.restaurante_servicio.actualizar_producto(
                codigo=datos["codigo"],
                nombre=datos["nombre"],
                categoria=datos["categoria"],
                precio=precio_val,
                stock=stock_val
            )
            self.cargar_productos()
            self._actualizar_metricas()
            self._cargar_opciones_combobox_ventas()
            self._mostrar_estado(f"✏️ ¡Producto [{producto_act.codigo}] actualizado correctamente!", "exito")
            messagebox.showinfo(
                "Actualización Exitosa",
                f"El producto [{producto_act.codigo}] ha sido actualizado en productos.json.",
                parent=self
            )
        except ValueError as e:
            self._mostrar_estado(f"❌ Error al actualizar: {e}", "error")
            messagebox.showwarning("Aviso de Validación", str(e), parent=self)
        except Exception as e:
            self._mostrar_estado(f"❌ Error al actualizar: {e}", "error")
            messagebox.showerror("Error", str(e), parent=self)

    def _eliminar_producto(self) -> None:
        """Acción del botón 'Eliminar' en Productos."""
        codigo = self.txt_codigo.get().strip()
        if not codigo:
            self._mostrar_estado("⚠️ Ingrese el código del producto que desea eliminar.", "advertencia")
            self.txt_codigo.focus_set()
            return

        producto = self.restaurante_servicio.buscar_producto(codigo)
        if producto is None:
            self._mostrar_estado(f"❌ No existe un producto con el código '{codigo}'.", "error")
            return

        confirmar = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el producto:\n\n[{producto.codigo}] {producto.nombre}?\n\nEsta acción modificará productos.json.",
            parent=self
        )
        if not confirmar:
            return

        try:
            prod_eliminado = self.restaurante_servicio.eliminar_producto(codigo)
            self.cargar_productos()
            self._actualizar_metricas()
            self._cargar_opciones_combobox_ventas()
            self._limpiar_formulario(mantener_estado=True)
            self._mostrar_estado(f"🗑️ Producto [{prod_eliminado.codigo}] eliminado del catálogo.", "info")
            messagebox.showinfo(
                "Producto Eliminado",
                f"El producto [{prod_eliminado.codigo}] '{prod_eliminado.nombre}' fue eliminado.",
                parent=self
            )
        except ValueError as e:
            self._mostrar_estado(f"❌ Error al eliminar: {e}", "error")
        except Exception as e:
            self._mostrar_estado(f"❌ Error: {e}", "error")

    def _cargar_seleccionado_de_tabla(self) -> None:
        """Carga los datos de la fila de producto seleccionada al formulario."""
        seleccion = self.tree_productos.selection()
        if not seleccion:
            self._mostrar_estado("⚠️ Seleccione una fila de la tabla y luego pulse este botón.", "advertencia")
            return

        item = self.tree_productos.item(seleccion[0])
        valores = item.get("values", [])
        if not valores:
            return

        codigo = str(valores[0])
        producto = self.restaurante_servicio.buscar_producto(codigo)
        if producto:
            self._llenar_formulario(producto)
            self._mostrar_estado(f"📋 Fila seleccionada [{producto.codigo}] cargada en el formulario.", "info")

    def _llenar_formulario(self, producto: Producto) -> None:
        """Escribe los atributos de un producto en los componentes del formulario."""
        self.txt_codigo.delete(0, tk.END)
        self.txt_codigo.insert(0, producto.codigo)

        self.txt_nombre.delete(0, tk.END)
        self.txt_nombre.insert(0, producto.nombre)

        self.cmb_categoria.set(producto.categoria)

        self.txt_precio.delete(0, tk.END)
        self.txt_precio.insert(0, f"{producto.precio:.2f}")

        self.txt_stock.delete(0, tk.END)
        self.txt_stock.insert(0, str(producto.stock))

    def _limpiar_formulario(self, mantener_estado: bool = False) -> None:
        """Limpia los campos del formulario de productos."""
        self.txt_codigo.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.cmb_categoria.set("Carnes")
        self.txt_precio.delete(0, tk.END)
        self.txt_stock.delete(0, tk.END)
        self.txt_codigo.focus_set()

        if not mantener_estado:
            self._mostrar_estado("Campos limpios. Ingrese datos para una nueva operación.", "info")

    def _mostrar_estado(self, mensaje: str, tipo: str = "info") -> None:
        """Muestra un mensaje visual en el banner de productos."""
        configuraciones = {
            "exito": {"bg": "#DCFCE7", "fg": "#14532D"},
            "error": {"bg": "#FEE2E2", "fg": "#991B1B"},
            "advertencia": {"bg": "#FEF3C7", "fg": "#92400E"},
            "info": {"bg": "#F1F5F9", "fg": "#334155"}
        }
        cfg = configuraciones.get(tipo, {"bg": "#F1F5F9", "fg": "#334155"})
        self.banner_estado.config(bg=cfg["bg"])
        self.lbl_estado_producto.config(text=mensaje, bg=cfg["bg"], fg=cfg["fg"])

    # =========================================================================
    # CARGA Y ACTUALIZACIÓN INTEGRAL DE DATOS
    # =========================================================================

    def cargar_datos_vistas(self) -> None:
        """Carga inicial de productos, usuarios, ventas y combos."""
        self.cargar_productos()
        self.cargar_usuarios()
        self.cargar_ventas()
        self._actualizar_metricas()
        self._actualizar_metricas_ventas()
        self._cargar_opciones_combobox_ventas()

    def cargar_productos(self) -> None:
        """Renderiza los productos en el Treeview correspondiente."""
        for item in self.tree_productos.get_children():
            self.tree_productos.delete(item)

        productos = self.restaurante_servicio.listar_productos()

        for idx, prod in enumerate(productos):
            tag = "fila_par" if idx % 2 == 0 else "fila_impar"
            self.tree_productos.insert(
                "",
                "end",
                values=(
                    prod.codigo,
                    prod.nombre,
                    prod.categoria,
                    f"${prod.precio:.2f}",
                    prod.stock
                ),
                tags=(tag,)
            )

        categorias_disponibles = self.restaurante_servicio.obtener_categorias_unicas()
        self.cmb_categoria["values"] = categorias_disponibles

    def cargar_usuarios(self) -> None:
        """Renderiza los usuarios en el Treeview correspondiente."""
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)

        usuarios = self.restaurante_servicio.listar_usuarios()

        for idx, usr in enumerate(usuarios):
            tag = "fila_par" if idx % 2 == 0 else "fila_impar"
            self.tree_usuarios.insert(
                "",
                "end",
                values=(
                    usr.identificacion,
                    usr.nombre,
                    usr.correo
                ),
                tags=(tag,)
            )

        self.lbl_metrica_usuarios.config(text=f"{len(usuarios)} usuarios")

    def cargar_ventas(self) -> None:
        """Renderiza las ventas en el Treeview de la pestaña de ventas."""
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)

        ventas = self.restaurante_servicio.listar_ventas()

        for idx, v in enumerate(ventas):
            tag = "fila_par" if idx % 2 == 0 else "fila_impar"
            self.tree_ventas.insert(
                "",
                "end",
                values=(
                    v.id_venta,
                    v.fecha,
                    v.nombre_usuario,
                    v.nombre_producto,
                    f"${v.precio_unitario:.2f}",
                    v.cantidad,
                    f"${v.total:.2f}"
                ),
                tags=(tag,)
            )

    def _actualizar_metricas(self) -> None:
        """Actualiza los indicadores de productos."""
        total_prods = self.restaurante_servicio.obtener_cantidad_productos()
        total_stock = self.restaurante_servicio.obtener_total_stock()
        categorias = len(self.restaurante_servicio.obtener_categorias_unicas())

        self.lbl_metrica_total.config(text=f"{total_prods} platos")
        self.lbl_metrica_stock.config(text=f"{total_stock} unidades")
        self.lbl_metrica_cat.config(text=f"{categorias} categorías")

    def _actualizar_metricas_ventas(self) -> None:
        """Actualiza los indicadores métricos de la pestaña de ventas."""
        total_ventas = self.restaurante_servicio.obtener_cantidad_ventas()
        total_ingresos = self.restaurante_servicio.obtener_total_ingresos_ventas()
        total_unidades = self.restaurante_servicio.obtener_total_unidades_vendidas()

        self.lbl_metrica_ventas_cant.config(text=f"{total_ventas} transacciones")
        self.lbl_metrica_ventas_ingresos.config(text=f"${total_ingresos:.2f}")
        self.lbl_metrica_ventas_unidades.config(text=f"{total_unidades} unidades")

    def _cargar_opciones_combobox_ventas(self) -> None:
        """Puebla los selectores desplegables de usuarios y productos para registrar ventas."""
        # Poblar usuarios
        usuarios = self.restaurante_servicio.listar_usuarios()
        self._mapa_usuarios_combo.clear()
        opciones_usr = []
        for u in usuarios:
            label = f"{u.nombre} (ID: {u.identificacion})"
            opciones_usr.append(label)
            self._mapa_usuarios_combo[label] = u.identificacion

        self.cmb_venta_usuario["values"] = opciones_usr
        if opciones_usr and not self.cmb_venta_usuario.get():
            self.cmb_venta_usuario.current(0)

        # Poblar productos
        productos = self.restaurante_servicio.listar_productos()
        self._mapa_productos_combo.clear()
        opciones_prd = []
        for p in productos:
            label = f"[{p.codigo}] {p.nombre} — ${p.precio:.2f} (Stock: {p.stock})"
            opciones_prd.append(label)
            self._mapa_productos_combo[label] = p.codigo

        self.cmb_venta_producto["values"] = opciones_prd
        if opciones_prd:
            # Preservar producto seleccionado si sigue existiendo
            actual = self.cmb_venta_producto.get()
            if actual in self._mapa_productos_combo:
                # Actualizar etiqueta con nuevo stock
                cod = self._mapa_productos_combo[actual]
                for opt in opciones_prd:
                    if self._mapa_productos_combo.get(opt) == cod:
                        self.cmb_venta_producto.set(opt)
                        break
            else:
                self.cmb_venta_producto.current(0)
            self._al_cambiar_seleccion_producto()

    # =========================================================================
    # CONTROL DE SESIÓN
    # =========================================================================

    def _confirmar_cierre_sesion(self) -> None:
        """Solicita confirmación antes de salir al Login."""
        confirmar = messagebox.askyesno(
            "Cerrar Sesión",
            "¿Desea cerrar la sesión activa y regresar a la pantalla de acceso?",
            parent=self
        )
        if confirmar:
            self.on_cerrar_sesion()
