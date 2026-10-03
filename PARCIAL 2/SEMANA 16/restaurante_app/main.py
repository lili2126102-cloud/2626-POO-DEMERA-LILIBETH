# -*- coding: utf-8 -*-
"""
Punto de Entrada Principal - Restaurante App (Semana 16)
======================================================
Asignatura: Programación Orientada a Objetos (UEA)
Estudiante: Lilibeth Demera

Orquestador principal de la aplicación:
1. Inicializa la instancia de la ventana única de Tkinter (tk.Tk) y carga el ícono corporativo desde assets/.
2. Configura los estilos ttk aplicando una paleta con armonía de colores pasteles.
3. Resuelve rutas relativas y prepara los servicios (ArchivoServicio y RestauranteServicio) con soporte de ventas.
4. Aplica Inyección de Dependencias a las vistas.
5. Gestiona el intercambio limpio y seguro entre LoginView y MainView.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

# Compatibilidad UTF-8 en consolas Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Asegurar que el directorio de la aplicación se encuentre en sys.path
DIRECTORIO_APP = os.path.dirname(os.path.abspath(__file__))
if DIRECTORIO_APP not in sys.path:
    sys.path.insert(0, DIRECTORIO_APP)

from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView


class AplicacionRestaurante:
    """
    Controlador maestro del ciclo de vida de la aplicación con Tkinter.
    Administra la ventana raíz, temas ttk, inyección de dependencias,
    recursos visuales de assets/ y navegación entre vistas.
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Inicializa la ventana principal, estilos y servicios.
        
        :param root: Instancia raíz de Tkinter.
        """
        self.root = root
        self.vista_actual: Optional[tk.Widget] = None
        self._icono_ventana: Optional[tk.PhotoImage] = None

        self._configurar_ventana()
        self._inicializar_servicios()

        # Contenedor dinámico intercambiable
        self.contenedor = ttk.Frame(self.root)
        self.contenedor.pack(fill="both", expand=True)

        # Iniciar mostrando la pantalla de login
        self.mostrar_login()

    def _configurar_ventana(self) -> None:
        """Establece títulos, dimensiones, estilos pasteles, ícono corporativo y centrado."""
        self.root.title("Restaurante Gourmet — Sistema de Gestión y Ventas (Semana 16)")
        ancho = 960
        alto = 680

        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        pos_x = max(0, (ancho_pantalla // 2) - (ancho // 2))
        pos_y = max(0, (alto_pantalla // 2) - (alto // 2))

        self.root.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")
        self.root.minsize(860, 600)

        # Cargar ícono de la ventana desde assets/
        ruta_icono = os.path.join(DIRECTORIO_APP, "assets", "icono_app.png")
        if os.path.exists(ruta_icono):
            try:
                self._icono_ventana = tk.PhotoImage(file=ruta_icono)
                self.root.iconphoto(True, self._icono_ventana)
            except Exception as e:
                print(f"[Aviso] No fue posible fijar el ícono de ventana: {e}")

        self.root.protocol("WM_DELETE_WINDOW", self._al_cerrar_ventana)

        # --- CONFIGURACIÓN DE ESTILOS TTK EN TONOS PASTELES ---
        self.estilos = ttk.Style(self.root)
        temas = self.estilos.theme_names()
        if "clam" in temas:
            self.estilos.theme_use("clam")

        # Configuración tipográfica base
        self.estilos.configure(".", font=("Segoe UI", 9))

        # Estilo para Pestañas (Notebook) en tonos pasteles
        self.estilos.configure(
            "TNotebook",
            background="#F8FAFC",
            borderwidth=0
        )
        self.estilos.configure(
            "TNotebook.Tab",
            padding=[16, 6],
            font=("Segoe UI", 9, "bold"),
            background="#E2E8F0",      # Gris pizarra pastel inactivo
            foreground="#475569"
        )
        self.estilos.map(
            "TNotebook.Tab",
            background=[("selected", "#FFFFFF"), ("active", "#EDE9FE")],
            foreground=[("selected", "#1E293B"), ("active", "#4C1D95")]
        )

        # Estilo para Treeview (Tablas) con encabezados suaves
        self.estilos.configure(
            "Treeview",
            rowheight=25,
            font=("Segoe UI", 9),
            background="#FFFFFF",
            fieldbackground="#FFFFFF"
        )
        self.estilos.configure(
            "Treeview.Heading",
            font=("Segoe UI", 9, "bold"),
            background="#E2E8F0",      # Encabezado pastel suave
            foreground="#1E293B",
            padding=5
        )

        # Estilo para LabelFrames
        self.estilos.configure(
            "TLabelframe",
            background="#FFFFFF"
        )
        self.estilos.configure(
            "TLabelframe.Label",
            font=("Segoe UI", 9, "bold"),
            foreground="#334155"
        )

    def _inicializar_servicios(self) -> None:
        """Inicializa ArchivoServicio y RestauranteServicio con persistencia JSON completa."""
        ruta_datos = os.path.join(DIRECTORIO_APP, "datos")
        ruta_productos = os.path.join(ruta_datos, "productos.json")
        ruta_usuarios = os.path.join(ruta_datos, "usuarios.json")
        ruta_ventas = os.path.join(ruta_datos, "ventas.json")

        self.archivo_servicio = ArchivoServicio(
            ruta_productos=ruta_productos,
            ruta_usuarios=ruta_usuarios,
            ruta_ventas=ruta_ventas
        )

        self.restaurante_servicio = RestauranteServicio(
            archivo_servicio=self.archivo_servicio
        )

        # Cargar los datos iniciales (productos, usuarios y ventas)
        self.restaurante_servicio.cargar_datos()

    # === Navegación de Vistas ===

    def mostrar_login(self) -> None:
        """Carga la pantalla de acceso LoginView en la ventana única."""
        self._limpiar_vista_actual()

        self.vista_actual = LoginView(
            parent=self.contenedor,
            restaurante_servicio=self.restaurante_servicio,
            on_login_exitoso=self.mostrar_main
        )
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_main(self, usuario: Usuario) -> None:
        """Carga el panel principal MainView tras el acceso exitoso."""
        self._limpiar_vista_actual()

        self.vista_actual = MainView(
            parent=self.contenedor,
            usuario_autenticado=usuario,
            restaurante_servicio=self.restaurante_servicio,
            on_cerrar_sesion=self.mostrar_login
        )
        self.vista_actual.pack(fill="both", expand=True)

    def _limpiar_vista_actual(self) -> None:
        """Destruye limpiamente la vista previa."""
        if self.vista_actual is not None:
            self.vista_actual.destroy()
            self.vista_actual = None

    def _al_cerrar_ventana(self) -> None:
        """Confirma el cierre seguro cuando el usuario está en el panel principal."""
        if isinstance(self.vista_actual, MainView):
            confirmar = messagebox.askyesno(
                "Salir del Sistema",
                "¿Desea cerrar el sistema de gestión del restaurante?",
                parent=self.root
            )
            if not confirmar:
                return
        self.root.destroy()


def main() -> None:
    """Función principal de ejecución del sistema."""
    root = tk.Tk()
    app = AplicacionRestaurante(root)
    root.mainloop()


if __name__ == "__main__":
    main()
