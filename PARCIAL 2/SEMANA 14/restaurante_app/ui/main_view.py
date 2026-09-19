# -*- coding: utf-8 -*-
"""
Panel Principal - Restaurante App (Semana 14)
=============================================
Implementa la interfaz principal del sistema aplicando componentes y contenedores
de Tkinter/ttk, una paleta de colores pasteles y operaciones CRUD sobre productos
delegadas exclusivamente al RestauranteServicio con persistencia en productos.json.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional
from modelos.usuario import Usuario
from modelos.producto import Producto
from servicios.restaurante_servicio import RestauranteServicio


class MainView(ttk.Frame):
    """
    Panel integral de administración del restaurante.
    Organizado mediante contenedores jerárquicos:
    - Barra superior (Header pastel con branding y sesión)
    - Pestañas de navegación (Notebook)
    - Sección de Productos: métricas, formulario grid, botonera pastel y tabla
    - Sección de Usuarios: consulta organizada con Treeview
    - Sección de Ventas: roadmap pedagógico
    - Barra de estado inferior
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

        self._configurar_interfaz()
        self.cargar_datos_vistas()

    def _configurar_interfaz(self) -> None:
        """Construye todos los contenedores y componentes de la vista principal."""
        self.pack(fill="both", expand=True)

        # ---------------------------------------------------------------------
        # 1. CONTENEDOR SUPERIOR: Header con colores pasteles suaves
        # ---------------------------------------------------------------------
        header_frame = tk.Frame(self, bg="#8FA4B5", height=58)  # Azul pizarra pastel
        header_frame.pack(fill="x", side="top")

        lbl_logo = tk.Label(
            header_frame,
            text="🍽️  RESTAURANTE GOURMET  •  SISTEMA DE GESTIÓN",
            font=("Segoe UI", 12, "bold"),
            fg="#FFFFFF",
            bg="#8FA4B5",
            padx=16,
            pady=10
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
            fg="#881337",              # Rojo borgoña suave legible
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
        self.notebook.add(self.tab_ventas, text="  🧾 Módulo de Ventas (Roadmap)  ")

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
            text="Semana 14 • POO UEA — Componentes, Contenedores y Persistencia JSON",
            font=("Segoe UI", 8),
            fg="#475569",
            bg="#E2E8F0",
            padx=12,
            pady=2
        )
        lbl_status.pack(side="left")

    # =========================================================================
    # PESTAÑA 1: GESTIÓN DE PRODUCTOS (CRUD, FORMULARIO Y CONTENEDORES)
    # =========================================================================

    def _construir_pestana_productos(self) -> None:
        """
        Construye la sección de productos dividida en 4 zonas de contenedores:
        A. Tarjetas métricas en colores pasteles.
        B. Formulario de captura y consulta con gestor de geometría Grid.
        C. Botonera de acciones con botones en tonos pasteles.
        D. Tabla de catálogo (Treeview) con scrollbar.
        """
        # --- ZONA A: Tarjetas Métricas Superiores (Colores pasteles) ---
        metricas_frame = tk.Frame(self.tab_productos, bg="#F1F5F9")
        metricas_frame.pack(fill="x", pady=(0, 8))

        # Tarjeta 1: Total Productos (Lavanda pastel)
        c1 = tk.Frame(metricas_frame, bg="#EDE9FE", bd=1, relief="solid")
        c1.pack(side="left", fill="both", expand=True, padx=4, pady=2)
        tk.Label(c1, text="📦 TOTAL PRODUCTOS", font=("Segoe UI", 8, "bold"), bg="#EDE9FE", fg="#5B21B6").pack(anchor="w", padx=8, pady=(4, 0))
        self.lbl_metrica_total = tk.Label(c1, text="0", font=("Segoe UI", 14, "bold"), bg="#EDE9FE", fg="#4C1D95")
        self.lbl_metrica_total.pack(anchor="w", padx=8, pady=(0, 4))

        # Tarjeta 2: Stock Acumulado (Menta pastel)
        c2 = tk.Frame(metricas_frame, bg="#DCFCE7", bd=1, relief="solid")
        c2.pack(side="left", fill="both", expand=True, padx=4, pady=2)
        tk.Label(c2, text="📊 STOCK ACUMULADO", font=("Segoe UI", 8, "bold"), bg="#DCFCE7", fg="#166534").pack(anchor="w", padx=8, pady=(4, 0))
        self.lbl_metrica_stock = tk.Label(c2, text="0 uds", font=("Segoe UI", 14, "bold"), bg="#DCFCE7", fg="#14532D")
        self.lbl_metrica_stock.pack(anchor="w", padx=8, pady=(0, 4))

        # Tarjeta 3: Categorías Activas (Ámbar / Durazno pastel)
        c3 = tk.Frame(metricas_frame, bg="#FEF3C7", bd=1, relief="solid")
        c3.pack(side="left", fill="both", expand=True, padx=4, pady=2)
        tk.Label(c3, text="🏷️ CATEGORÍAS DISPONIBLES", font=("Segoe UI", 8, "bold"), bg="#FEF3C7", fg="#92400E").pack(anchor="w", padx=8, pady=(4, 0))
        self.lbl_metrica_cat = tk.Label(c3, text="0 categorías", font=("Segoe UI", 14, "bold"), bg="#FEF3C7", fg="#78350F")
        self.lbl_metrica_cat.pack(anchor="w", padx=8, pady=(0, 4))

        # --- ZONA B: Formulario de Entrada (LabelFrame con Grid) ---
        self.form_frame = ttk.LabelFrame(
            self.tab_productos,
            text=" 📋 Formulario de Producto (Registro / Consulta / Edición) ",
            padding=(12, 8)
        )
        self.form_frame.pack(fill="x", pady=(0, 8))

        # Configurar pesos de columnas para distribución uniforme
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

        # Mensaje de ayuda / instrucción rápida
        lbl_pista = ttk.Label(
            self.form_frame,
            text="💡 Ingrese el Código y use 'Cargar' para consultar datos, o 'Registrar' para un producto nuevo.",
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
            bg="#A7F3D0",              # Verde menta pastel
            fg="#065F46",              # Verde oscuro suave
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
            bg="#BAE6FD",              # Azul cielo pastel
            fg="#075985",              # Azul marino suave
            activebackground="#7DD3FC",
            activeforeground="#0C4A6E",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=4,
            command=self._cargar_o_consultar_producto
        )
        self.btn_consultar.pack(side="left", padx=4)

        # Botón 3: ACTUALIZAR (Pastel Durazno / Ámbar)
        self.btn_actualizar = tk.Button(
            acciones_frame,
            text="✏️ Actualizar",
            font=("Segoe UI", 9, "bold"),
            bg="#FED7AA",              # Durazno pastel
            fg="#9A3412",              # Café-naranja suave
            activebackground="#FDBA74",
            activeforeground="#7C2D12",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=4,
            command=self._actualizar_producto
        )
        self.btn_actualizar.pack(side="left", padx=4)

        # Botón 4: ELIMINAR (Pastel Rosa / Coral)
        self.btn_eliminar = tk.Button(
            acciones_frame,
            text="🗑️ Eliminar",
            font=("Segoe UI", 9, "bold"),
            bg="#FECDD3",              # Rosa pastel
            fg="#9F1239",              # Rojo vino suave
            activebackground="#FDA4AF",
            activeforeground="#881337",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=4,
            command=self._eliminar_producto
        )
        self.btn_eliminar.pack(side="left", padx=4)

        # Botón 5: LIMPIAR (Pastel Gris / Lavanda)
        self.btn_limpiar = tk.Button(
            acciones_frame,
            text="🧹 Limpiar Campos",
            font=("Segoe UI", 9),
            bg="#E2E8F0",              # Gris claro pastel
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
            bg="#E9D5FF",              # Lila/Lavanda pastel
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
            height=9
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

        # Configurar colores alternados en filas para estética limpia
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

        # Tarjeta métrica de usuarios en tono pastel suave
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
            height=14
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
    # PESTAÑA 3: VENTAS (ROADMAP PEDAGÓGICO)
    # =========================================================================

    def _construir_pestana_ventas(self) -> None:
        """Presenta el módulo de ventas claramente identificado como funcionalidad futura."""
        contenedor = ttk.Frame(self.tab_ventas, padding=25)
        contenedor.pack(fill="both", expand=True)

        lbl_icono = ttk.Label(
            contenedor,
            text="⏳ 🧾",
            font=("Segoe UI Emoji", 34)
        )
        lbl_icono.pack(pady=(10, 6))

        lbl_titulo = ttk.Label(
            contenedor,
            text="Módulo Transaccional de Ventas — Hoja de Ruta",
            font=("Segoe UI", 13, "bold"),
            foreground="#1E293B"
        )
        lbl_titulo.pack(pady=(0, 6))

        texto = (
            "En la presente Semana 14 el objetivo central del diseño es consolidar el uso "
            "adecuado de Componentes y Contenedores (Frame, LabelFrame, Notebook, Treeview, "
            "Combobox, Entry y botones con command=) y afianzar la persistencia en archivos JSON "
            "a través de la capa de servicios.\n\n"
            "El flujo transaccional de ventas, la facturación electrónica y la emisión de comandas "
            "se integrarán progresivamente en las próximas entregas del curso."
        )
        lbl_desc = ttk.Label(
            contenedor,
            text=texto,
            font=("Segoe UI", 9),
            wraplength=550,
            justify="center",
            foreground="#475569"
        )
        lbl_desc.pack(pady=(0, 16))

        tarjeta_info = ttk.LabelFrame(contenedor, text=" 🚀 Próximos Desarrollos Planificados ", padding=12)
        tarjeta_info.pack(fill="x", padx=40)

        proximos = (
            "• Carrito interactivo de pedidos para mesas de salón y pedidos para llevar.\n"
            "• Reducción automática de existencias en tiempo real al concretar la orden.\n"
            "• Historial de consumo por cliente y cálculo dinámico de impuestos (IVA).\n"
            "• Exportación de comprobantes y reportes financieros."
        )
        lbl_proximos = ttk.Label(
            tarjeta_info,
            text=proximos,
            font=("Segoe UI", 9),
            foreground="#334155",
            justify="left"
        )
        lbl_proximos.pack(anchor="w")

    # =========================================================================
    # OPERACIONES CRUD SOBRE PRODUCTOS (DELEGADAS A RESTAURANTESERVICIO)
    # =========================================================================

    def _obtener_datos_formulario(self) -> dict:
        """
        Recupera y limpia los valores de los campos del formulario.
        No realiza validaciones complejas de dominio; esas corresponden al servicio.
        """
        return {
            "codigo": self.txt_codigo.get().strip(),
            "nombre": self.txt_nombre.get().strip(),
            "categoria": self.cmb_categoria.get().strip(),
            "precio": self.txt_precio.get().strip(),
            "stock": self.txt_stock.get().strip()
        }

    def _registrar_producto(self) -> None:
        """
        Acción del botón 'Registrar':
        Captura los datos del formulario y solicita el registro a RestauranteServicio.
        """
        datos = self._obtener_datos_formulario()

        # Validación visual básica de presencia de campos
        if not datos["codigo"] or not datos["nombre"] or not datos["precio"] or not datos["stock"]:
            self._mostrar_estado("⚠️ Todos los campos son obligatorios para registrar un producto.", "advertencia")
            return

        try:
            precio_val = float(datos["precio"])
            stock_val = int(datos["stock"])
        except ValueError:
            self._mostrar_estado("⚠️ El precio debe ser un número decimal y el stock un número entero.", "advertencia")
            return

        # Delegar al servicio
        try:
            nuevo_prod = self.restaurante_servicio.registrar_producto(
                codigo=datos["codigo"],
                nombre=datos["nombre"],
                categoria=datos["categoria"],
                precio=precio_val,
                stock=stock_val
            )
            # Actualizar interfaz
            self.cargar_productos()
            self._actualizar_metricas()
            self._mostrar_estado(f"✅ ¡Producto '{nuevo_prod.nombre}' [{nuevo_prod.codigo}] registrado y guardado exitosamente!", "exito")
            messagebox.showinfo(
                "Registro Exitoso",
                f"El producto '{nuevo_prod.nombre}' con código [{nuevo_prod.codigo}] fue registrado y guardado en productos.json.",
                parent=self
            )
            self._limpiar_formulario(mantener_estado=True)
        except ValueError as e:
            self._mostrar_estado(f"❌ Error de validación: {e}", "error")
            messagebox.showwarning("Aviso de Validación", str(e), parent=self)
        except Exception as e:
            self._mostrar_estado(f"❌ Error al registrar: {e}", "error")
            messagebox.showerror("Error del Sistema", str(e), parent=self)

    def _cargar_o_consultar_producto(self) -> None:
        """
        Acción del botón 'Cargar / Consultar':
        Toma el código ingresado en el campo de código, consulta al servicio
        y carga los datos en el formulario para inspección o edición.
        """
        codigo = self.txt_codigo.get().strip()
        if not codigo:
            self._mostrar_estado("⚠️ Ingrese el código del producto a consultar en el campo 'Código'.", "advertencia")
            self.txt_codigo.focus_set()
            return

        producto = self.restaurante_servicio.buscar_producto(codigo)
        if producto is None:
            self._mostrar_estado(f"❌ No se encontró ningún producto con el código '{codigo.upper()}'.", "error")
            messagebox.showinfo("Búsqueda de Producto", f"No existe un producto con el código '{codigo.upper()}'.", parent=self)
            return

        # Cargar los datos en los componentes del formulario
        self._llenar_formulario(producto)
        self._mostrar_estado(f"🔍 Producto '{producto.nombre}' [{producto.codigo}] cargado en el formulario.", "info")

    def _actualizar_producto(self) -> None:
        """
        Acción del botón 'Actualizar':
        Toma los datos del formulario y solicita la modificación a RestauranteServicio.
        """
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
            # Actualizar interfaz
            self.cargar_productos()
            self._actualizar_metricas()
            self._mostrar_estado(f"✏️ ¡Producto [{producto_act.codigo}] actualizado correctamente!", "exito")
            messagebox.showinfo(
                "Actualización Exitosa",
                f"El producto [{producto_act.codigo}] ha sido actualizado y los cambios se guardaron en productos.json.",
                parent=self
            )
        except ValueError as e:
            self._mostrar_estado(f"❌ Error al actualizar: {e}", "error")
            messagebox.showwarning("Aviso de Validación", str(e), parent=self)
        except Exception as e:
            self._mostrar_estado(f"❌ Error al actualizar: {e}", "error")
            messagebox.showerror("Error", str(e), parent=self)

    def _eliminar_producto(self) -> None:
        """
        Acción del botón 'Eliminar':
        Solicita confirmación de seguridad y luego pide al servicio remover el producto.
        """
        codigo = self.txt_codigo.get().strip()
        if not codigo:
            self._mostrar_estado("⚠️ Ingrese el código del producto que desea eliminar (o cárguelo con 'Cargar').", "advertencia")
            self.txt_codigo.focus_set()
            return

        producto = self.restaurante_servicio.buscar_producto(codigo)
        if producto is None:
            self._mostrar_estado(f"❌ No existe un producto con el código '{codigo}'.", "error")
            return

        # Confirmación de seguridad
        confirmar = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de eliminar el producto:\n\n[{producto.codigo}] {producto.nombre}?\n\nEsta acción modificará el archivo productos.json.",
            parent=self
        )
        if not confirmar:
            return

        try:
            prod_eliminado = self.restaurante_servicio.eliminar_producto(codigo)
            self.cargar_productos()
            self._actualizar_metricas()
            self._limpiar_formulario(mantener_estado=True)
            self._mostrar_estado(f"🗑️ Producto [{prod_eliminado.codigo}] '{prod_eliminado.nombre}' eliminado del inventario.", "info")
            messagebox.showinfo(
                "Producto Eliminado",
                f"El producto [{prod_eliminado.codigo}] '{prod_eliminado.nombre}' fue eliminado correctamente.",
                parent=self
            )
        except ValueError as e:
            self._mostrar_estado(f"❌ Error al eliminar: {e}", "error")
        except Exception as e:
            self._mostrar_estado(f"❌ Error: {e}", "error")

    def _cargar_seleccionado_de_tabla(self) -> None:
        """
        Carga los datos de la fila actualmente seleccionada en el Treeview al formulario.
        Permite al usuario interactuar fluidamente sin requerir eventos complejos de mouse.
        """
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
        """Limpia todos los campos de entrada del formulario de producto."""
        self.txt_codigo.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.cmb_categoria.set("Carnes")
        self.txt_precio.delete(0, tk.END)
        self.txt_stock.delete(0, tk.END)
        self.txt_codigo.focus_set()

        if not mantener_estado:
            self._mostrar_estado("Campos limpios. Ingrese datos para una nueva operación.", "info")

    def _mostrar_estado(self, mensaje: str, tipo: str = "info") -> None:
        """
        Muestra un mensaje visual en el banner de estado con tonos pasteles de fondo.
        """
        configuraciones = {
            "exito": {"bg": "#DCFCE7", "fg": "#14532D"},       # Verde menta pastel
            "error": {"bg": "#FEE2E2", "fg": "#991B1B"},       # Rojo suave pastel
            "advertencia": {"bg": "#FEF3C7", "fg": "#92400E"}, # Ámbar pastel
            "info": {"bg": "#F1F5F9", "fg": "#334155"}          # Pizarra claro
        }
        cfg = configuraciones.get(tipo, {"bg": "#F1F5F9", "fg": "#334155"})
        self.banner_estado.config(bg=cfg["bg"])
        self.lbl_estado_producto.config(text=mensaje, bg=cfg["bg"], fg=cfg["fg"])

    # =========================================================================
    # CARGA Y PRESENTACIÓN DE DATOS (TREEVIEWS Y RESÚMENES)
    # =========================================================================

    def cargar_datos_vistas(self) -> None:
        """Carga los datos iniciales en productos y usuarios."""
        self.cargar_productos()
        self.cargar_usuarios()
        self._actualizar_metricas()

    def cargar_productos(self) -> None:
        """
        Consulta los productos a RestauranteServicio y los renderiza en el Treeview.
        Garantiza que la UI no lea directamente el archivo JSON.
        """
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

        # Actualizar opciones del combobox de categorías según catálogo
        categorias_disponibles = self.restaurante_servicio.obtener_categorias_unicas()
        self.cmb_categoria["values"] = categorias_disponibles

    def cargar_usuarios(self) -> None:
        """Consulta los usuarios a RestauranteServicio y los muestra en la tabla."""
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

    def _actualizar_metricas(self) -> None:
        """Calcula y actualiza los indicadores superiores en las tarjetas pasteles."""
        total_prods = self.restaurante_servicio.obtener_cantidad_productos()
        total_stock = self.restaurante_servicio.obtener_total_stock()
        categorias = len(self.restaurante_servicio.obtener_categorias_unicas())

        self.lbl_metrica_total.config(text=f"{total_prods} platos")
        self.lbl_metrica_stock.config(text=f"{total_stock} unidades")
        self.lbl_metrica_cat.config(text=f"{categorias} categorías")

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
