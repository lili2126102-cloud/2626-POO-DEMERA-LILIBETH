# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio

class LoginView(ttk.Frame):
    """
    Vista de inicio de sesión simulada desarrollada con componentes de Tkinter.
    Presenta los campos de captura de usuario y contraseña, muestra respuestas
    visuales claras ante errores o campos vacíos, y delega la validación de
    credenciales al RestauranteServicio.
    """

    def __init__(
        self,
        parent: tk.Widget,
        restaurante_servicio: RestauranteServicio,
        on_login_exitoso: Callable[[Usuario], None]
    ) -> None:
        """
        Inicializa la vista de Login.
        
        :param parent: Contenedor padre de Tkinter.
        :param restaurante_servicio: Instancia del servicio para validar credenciales.
        :param on_login_exitoso: Callback que se ejecuta cuando el acceso es correcto.
        """
        super().__init__(parent)
        self.restaurante_servicio = restaurante_servicio
        self.on_login_exitoso = on_login_exitoso

        self._configurar_interfaz()

    def _configurar_interfaz(self) -> None:
        """Construye y distribuye los componentes gráficos de la pantalla de login."""
        # Configurar expansión del frame
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Contenedor central (tarjeta con aspecto limpio y profesional)
        tarjeta = ttk.LabelFrame(self, text=" Acceso al Sistema ", padding=25)
        tarjeta.grid(row=0, column=0, padx=20, pady=20)

        # Encabezado / Branding
        lbl_icono = ttk.Label(
            tarjeta,
            text="🍽️",
            font=("Segoe UI Emoji", 32)
        )
        lbl_icono.pack(pady=(0, 5))

        lbl_titulo = ttk.Label(
            tarjeta,
            text="Restaurante Gourmet",
            font=("Segoe UI", 16, "bold")
        )
        lbl_titulo.pack()

        lbl_subtitulo = ttk.Label(
            tarjeta,
            text="Semana 13 • Módulo Gráfico Base",
            font=("Segoe UI", 9),
            foreground="#555555"
        )
        lbl_subtitulo.pack(pady=(2, 20))

        # Marco del formulario
        form_frame = ttk.Frame(tarjeta)
        form_frame.pack(fill="x", expand=True)

        # Campo: Usuario / Correo
        lbl_usuario = ttk.Label(
            form_frame,
            text="Usuario / Correo electrónico:",
            font=("Segoe UI", 10, "bold")
        )
        lbl_usuario.pack(anchor="w", pady=(0, 4))

        self.txt_usuario = ttk.Entry(form_frame, width=32, font=("Segoe UI", 10))
        self.txt_usuario.pack(fill="x", pady=(0, 12))
        self.txt_usuario.bind("<Return>", lambda event: self._procesar_login())

        # Campo: Contraseña
        lbl_clave = ttk.Label(
            form_frame,
            text="Contraseña de acceso:",
            font=("Segoe UI", 10, "bold")
        )
        lbl_clave.pack(anchor="w", pady=(0, 4))

        self.txt_clave = ttk.Entry(form_frame, width=32, font=("Segoe UI", 10), show="•")
        self.txt_clave.pack(fill="x", pady=(0, 10))
        self.txt_clave.bind("<Return>", lambda event: self._procesar_login())

        # Etiqueta para mensajes y feedback visual
        self.lbl_mensaje = ttk.Label(
            tarjeta,
            text="",
            font=("Segoe UI", 9, "italic"),
            wraplength=280,
            justify="center"
        )
        self.lbl_mensaje.pack(pady=(5, 12), fill="x")

        # Botón de Ingreso
        self.btn_ingresar = tk.Button(
            tarjeta,
            text="Iniciar Sesión",
            font=("Segoe UI", 10, "bold"),
            bg="#2B6CB0",
            fg="white",
            activebackground="#2C5282",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=6,
            command=self._procesar_login
        )
        self.btn_ingresar.pack(fill="x", pady=(0, 15))

        # Panel de ayuda con credenciales de prueba
        ayuda_frame = ttk.LabelFrame(tarjeta, text=" Credenciales de Prueba ", padding=8)
        ayuda_frame.pack(fill="x")

        txt_ayuda = (
            "• Usuario: lilibeth.d@gourmet.com | Clave: 1234\n"
            "• Usuario: juan.perez@gourmet.com   | Clave: admin123"
        )
        lbl_ayuda = ttk.Label(
            ayuda_frame,
            text=txt_ayuda,
            font=("Consolas", 8),
            foreground="#4A5568",
            justify="left"
        )
        lbl_ayuda.pack(anchor="w")

        btn_autollenar = ttk.Button(
            ayuda_frame,
            text="Usar credenciales de demostración",
            command=self._autollenar_demo
        )
        btn_autollenar.pack(fill="x", pady=(6, 0))

        # Foco inicial
        self.txt_usuario.focus_set()

    def _autollenar_demo(self) -> None:
        """Autollena el formulario con las credenciales demo para facilitar la revisión."""
        self.txt_usuario.delete(0, tk.END)
        self.txt_usuario.insert(0, "lilibeth.d@gourmet.com")
        self.txt_clave.delete(0, tk.END)
        self.txt_clave.insert(0, "1234")
        self.mostrar_mensaje("Credenciales cargadas. Presione 'Iniciar Sesión'.", tipo="info")

    def _procesar_login(self) -> None:
        """
        Valida que los campos no estén vacíos y consulta al RestauranteServicio
        para comprobar las credenciales del usuario.
        """
        usuario_val = self.txt_usuario.get().strip()
        clave_val = self.txt_clave.get().strip()

        # Validación 1: Campos vacíos
        if not usuario_val or not clave_val:
            self.mostrar_mensaje(
                "⚠️ Por favor, ingrese tanto el usuario como la contraseña.",
                tipo="advertencia"
            )
            if not usuario_val:
                self.txt_usuario.focus_set()
            else:
                self.txt_clave.focus_set()
            return

        # Validación 2: Verificación a través del servicio
        usuario_encontrado = self.restaurante_servicio.validar_acceso(usuario_val, clave_val)

        if usuario_encontrado is None:
            self.mostrar_mensaje(
                "❌ Credenciales incorrectas. Verifique su usuario o clave.",
                tipo="error"
            )
            self.txt_clave.delete(0, tk.END)
            self.txt_clave.focus_set()
            return

        # Acceso concedido
        self.mostrar_mensaje(
            f"✅ ¡Bienvenido(a), {usuario_encontrado.nombre}!",
            tipo="exito"
        )
        # Notificar a la ventana principal para alternar a MainView
        self.after(200, lambda: self.on_login_exitoso(usuario_encontrado))

    def mostrar_mensaje(self, mensaje: str, tipo: str = "info") -> None:
        """
        Muestra una respuesta visual adecuada según el resultado de la operación.
        """
        colores = {
            "error": "#C53030",       # Rojo oscuro
            "advertencia": "#DD6B20", # Naranja
            "exito": "#276749",       # Verde oscuro
            "info": "#2B6CB0"         # Azul
        }
        color = colores.get(tipo, "#2D3748")
        self.lbl_mensaje.config(text=mensaje, foreground=color)

    def limpiar_campos(self) -> None:
        """Limpia los campos del formulario y restablece el estado."""
        self.txt_usuario.delete(0, tk.END)
        self.txt_clave.delete(0, tk.END)
        self.lbl_mensaje.config(text="")
        self.txt_usuario.focus_set()
