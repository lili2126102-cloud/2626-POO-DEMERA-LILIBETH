# -*- coding: utf-8 -*-
"""
Vista de Inicio de Sesión - Restaurante App (Semana 14)
======================================================
Implementa la interfaz de acceso utilizando componentes y contenedores de Tkinter/ttk
con una estética agradable en tonos pasteles, retroalimentación visual clara y
delegación de validaciones al RestauranteServicio.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable
from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio


class LoginView(ttk.Frame):
    """
    Vista gráfica para el inicio de sesión.
    Organizada mediante contenedores y adaptada a la paleta de colores pasteles.
    """

    def __init__(
        self,
        parent: tk.Widget,
        restaurante_servicio: RestauranteServicio,
        on_login_exitoso: Callable[[Usuario], None]
    ) -> None:
        """
        Inicializa la vista de acceso.
        
        :param parent: Contenedor padre de Tkinter.
        :param restaurante_servicio: Servicio para validar las credenciales.
        :param on_login_exitoso: Callback que se ejecuta cuando el acceso es correcto.
        """
        super().__init__(parent)
        self.restaurante_servicio = restaurante_servicio
        self.on_login_exitoso = on_login_exitoso

        self._configurar_interfaz()

    def _configurar_interfaz(self) -> None:
        """Construye y distribuye los componentes y contenedores de la pantalla de login."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Fondo general suave
        self.configure(style="TFrame")

        # Contenedor central (tarjeta pastel estilizada)
        tarjeta = ttk.LabelFrame(
            self,
            text=" 🔐 Acceso al Sistema ",
            padding=25
        )
        tarjeta.grid(row=0, column=0, padx=20, pady=20)

        # Encabezado con ícono y títulos
        lbl_icono = ttk.Label(
            tarjeta,
            text="🍽️",
            font=("Segoe UI Emoji", 34)
        )
        lbl_icono.pack(pady=(0, 4))

        lbl_titulo = ttk.Label(
            tarjeta,
            text="Restaurante Gourmet",
            font=("Segoe UI", 16, "bold"),
            foreground="#2C3E50"
        )
        lbl_titulo.pack()

        lbl_subtitulo = ttk.Label(
            tarjeta,
            text="Semana 14 • Componentes y Contenedores",
            font=("Segoe UI", 9),
            foreground="#64748B"
        )
        lbl_subtitulo.pack(pady=(2, 18))

        # Contenedor del Formulario
        form_frame = ttk.Frame(tarjeta)
        form_frame.pack(fill="x", expand=True)

        # Campo: Usuario / Correo
        lbl_usuario = ttk.Label(
            form_frame,
            text="Usuario / Correo electrónico:",
            font=("Segoe UI", 9, "bold"),
            foreground="#334155"
        )
        lbl_usuario.pack(anchor="w", pady=(0, 3))

        self.txt_usuario = ttk.Entry(form_frame, width=34, font=("Segoe UI", 10))
        self.txt_usuario.pack(fill="x", pady=(0, 10))
        self.txt_usuario.bind("<Return>", lambda _: self._procesar_login())

        # Campo: Contraseña
        lbl_clave = ttk.Label(
            form_frame,
            text="Contraseña de acceso:",
            font=("Segoe UI", 9, "bold"),
            foreground="#334155"
        )
        lbl_clave.pack(anchor="w", pady=(0, 3))

        self.txt_clave = ttk.Entry(form_frame, width=34, font=("Segoe UI", 10), show="•")
        self.txt_clave.pack(fill="x", pady=(0, 10))
        self.txt_clave.bind("<Return>", lambda _: self._procesar_login())

        # Etiqueta de mensaje de estado
        self.lbl_mensaje = ttk.Label(
            tarjeta,
            text="",
            font=("Segoe UI", 9, "italic"),
            wraplength=290,
            justify="center"
        )
        self.lbl_mensaje.pack(pady=(2, 10), fill="x")

        # Botón de Ingreso con tono pastel elegante (azul suave pastel)
        self.btn_ingresar = tk.Button(
            tarjeta,
            text="🚀  Iniciar Sesión",
            font=("Segoe UI", 10, "bold"),
            bg="#93C5FD",              # Azul pastel cielo
            fg="#1E3A8A",              # Azul marino legible
            activebackground="#BFDBFE",
            activeforeground="#1E3A8A",
            relief="flat",
            cursor="hand2",
            padx=16,
            pady=7,
            command=self._procesar_login
        )
        self.btn_ingresar.pack(fill="x", pady=(0, 14))

        # Contenedor de ayuda con credenciales de prueba en tono pastel suave
        ayuda_frame = ttk.LabelFrame(tarjeta, text=" 💡 Credenciales de Prueba ", padding=10)
        ayuda_frame.pack(fill="x")

        txt_ayuda = (
            "• Usuario: lilibeth.d@gourmet.com  |  Clave: 1234\n"
            "• Usuario: juan.perez@gourmet.com    |  Clave: admin123\n"
            "• Usuario: 1700000003                 |  Clave: gourmet2026"
        )
        lbl_ayuda = ttk.Label(
            ayuda_frame,
            text=txt_ayuda,
            font=("Consolas", 8),
            foreground="#475569",
            justify="left"
        )
        lbl_ayuda.pack(anchor="w")

        # Botón para autollenar demo en tono lavanda pastel
        btn_autollenar = tk.Button(
            ayuda_frame,
            text="Autollenar cuenta demostración",
            font=("Segoe UI", 8),
            bg="#E0E7FF",              # Lavanda/índigo pastel
            fg="#3730A3",
            activebackground="#C7D2FE",
            activeforeground="#312E81",
            relief="flat",
            cursor="hand2",
            padx=8,
            pady=4,
            command=self._autollenar_demo
        )
        btn_autollenar.pack(fill="x", pady=(8, 0))

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
        Valida que los campos no estén vacíos y solicita la verificación
        al RestauranteServicio sin acceder directamente a los datos.
        """
        usuario_val = self.txt_usuario.get().strip()
        clave_val = self.txt_clave.get().strip()

        if not usuario_val or not clave_val:
            self.mostrar_mensaje(
                "⚠️ Ingrese tanto el usuario/correo como la contraseña.",
                tipo="advertencia"
            )
            if not usuario_val:
                self.txt_usuario.focus_set()
            else:
                self.txt_clave.focus_set()
            return

        usuario_encontrado = self.restaurante_servicio.validar_acceso(usuario_val, clave_val)

        if usuario_encontrado is None:
            self.mostrar_mensaje(
                "❌ Credenciales incorrectas. Verifique sus datos.",
                tipo="error"
            )
            self.txt_clave.delete(0, tk.END)
            self.txt_clave.focus_set()
            return

        self.mostrar_mensaje(
            f"✅ ¡Bienvenido(a), {usuario_encontrado.nombre}!",
            tipo="exito"
        )
        # Notificar a la ventana principal para alternar a MainView
        self.after(200, lambda: self.on_login_exitoso(usuario_encontrado))

    def mostrar_mensaje(self, mensaje: str, tipo: str = "info") -> None:
        """Presenta retroalimentación visual con colores pasteles/claros según el tipo."""
        colores = {
            "error": "#B91C1C",       # Rojo oscuro sobre texto
            "advertencia": "#C2410C", # Naranja
            "exito": "#15803D",       # Verde oscuro sobre texto
            "info": "#1D4ED8"         # Azul
        }
        color = colores.get(tipo, "#334155")
        self.lbl_mensaje.config(text=mensaje, foreground=color)

    def limpiar_campos(self) -> None:
        """Limpia los campos del formulario."""
        self.txt_usuario.delete(0, tk.END)
        self.txt_clave.delete(0, tk.END)
        self.lbl_mensaje.config(text="")
        self.txt_usuario.focus_set()
