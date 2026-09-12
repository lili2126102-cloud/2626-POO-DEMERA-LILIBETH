# -*- coding: utf-8 -*-
"""
Punto de Entrada Principal - Restaurante App (Semana 13)
======================================================
Asignatura: Programación Orientada a Objetos (UEA)
Estudiante: Lilibeth Demera

Este archivo actúa como orquestador y punto de inicio del sistema:
1. Crea la única ventana principal de Tkinter (tk.Tk).
2. Resuelve de forma robusta las rutas locales de los archivos JSON.
3. Prepara las instancias de los servicios (ArchivoServicio y RestauranteServicio).
4. Entrega esas dependencias a las vistas (Inyección de Dependencias).
5. Controla el intercambio dinámico entre la pantalla de acceso (LoginView)
   y la interfaz principal (MainView) dentro del mismo marco de ventana.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

# Asegurar compatibilidad de codificación UTF-8 en consolas Windows
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
    Controlador principal de la aplicación con Tkinter.
    Administra el ciclo de vida de la ventana, la inyección de servicios
    y la alternancia de vistas en el contenedor maestro.
    """

    def __init__(self, root: tk.Tk) -> None:
        """
        Inicializa la aplicación, configura la ventana principal y prepara los servicios.
        
        :param root: Ventana principal de Tkinter.
        """
        self.root = root
        self.vista_actual: Optional[tk.Widget] = None

        self._configurar_ventana()
        self._inicializar_servicios()

        # Contenedor raíz donde se montarán las vistas de forma intercambiable
        self.contenedor = ttk.Frame(self.root)
        self.contenedor.pack(fill="both", expand=True)

        # Mostrar inicialmente la pantalla de acceso (LoginView)
        self.mostrar_login()

    def _configurar_ventana(self) -> None:
        """Establece títulos, dimensiones, estilos y centrado en pantalla."""
        self.root.title("Restaurante Gourmet — Sistema de Gestión (Semana 13)")
        ancho = 860
        alto = 620

        # Calcular posición para centrar la ventana en el monitor
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        pos_x = (ancho_pantalla // 2) - (ancho // 2)
        pos_y = (alto_pantalla // 2) - (alto // 2)

        self.root.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")
        self.root.minsize(760, 520)

        # Configurar protocolo de cierre seguro
        self.root.protocol("WM_DELETE_WINDOW", self._al_cerrar_ventana)

        # Configuración de estilos ttk
        self.estilos = ttk.Style(self.root)
        temas_disponibles = self.estilos.theme_names()
        if "clam" in temas_disponibles:
            self.estilos.theme_use("clam")

        # Ajustes de fuentes y componentes
        self.estilos.configure(".", font=("Segoe UI", 9))
        self.estilos.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), padding=4)
        self.estilos.configure("Treeview", rowheight=24)
        self.estilos.configure("TNotebook.Tab", padding=[15, 6], font=("Segoe UI", 9, "bold"))

    def _inicializar_servicios(self) -> None:
        """
        Prepara las dependencias de persistencia y lógica de negocio.
        Resuelve las rutas de los archivos JSON de forma dinámica.
        """
        ruta_datos = os.path.join(DIRECTORIO_APP, "datos")
        ruta_productos = os.path.join(ruta_datos, "productos.json")
        ruta_usuarios = os.path.join(ruta_datos, "usuarios.json")

        # 1. Instanciar servicio de persistencia
        self.archivo_servicio = ArchivoServicio(
            ruta_productos=ruta_productos,
            ruta_usuarios=ruta_usuarios
        )

        # 2. Instanciar servicio del restaurante inyectando la persistencia
        self.restaurante_servicio = RestauranteServicio(
            archivo_servicio=self.archivo_servicio
        )

        # 3. Cargar la información inicial
        self.restaurante_servicio.cargar_datos()

    # === Navegación y Cambio de Vistas dentro de la Misma Ventana ===

    def mostrar_login(self) -> None:
        """
        Monta la pantalla de acceso en la ventana principal.
        Elimina la vista previa para garantizar el uso de una única ventana de Tkinter.
        """
        self._limpiar_vista_actual()

        # Instanciar LoginView entregando el servicio y el callback de navegación
        self.vista_actual = LoginView(
            parent=self.contenedor,
            restaurante_servicio=self.restaurante_servicio,
            on_login_exitoso=self.mostrar_main
        )
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_main(self, usuario: Usuario) -> None:
        """
        Monta el panel principal tras una autenticación exitosa.
        Entrega la referencia del usuario conectado, el servicio y el callback para cerrar sesión.
        
        :param usuario: Objeto del usuario autenticado.
        """
        self._limpiar_vista_actual()

        # Instanciar MainView con dependencias
        self.vista_actual = MainView(
            parent=self.contenedor,
            usuario_autenticado=usuario,
            restaurante_servicio=self.restaurante_servicio,
            on_cerrar_sesion=self.mostrar_login
        )
        self.vista_actual.pack(fill="both", expand=True)

    def _limpiar_vista_actual(self) -> None:
        """Destruye de forma segura la vista desplegada actualmente en el contenedor."""
        if self.vista_actual is not None:
            self.vista_actual.destroy()
            self.vista_actual = None

    def _al_cerrar_ventana(self) -> None:
        """Maneja el evento de cierre de la ventana con confirmación si está en MainView."""
        if isinstance(self.vista_actual, MainView):
            confirmar = messagebox.askyesno(
                "Salir de la Aplicación",
                "¿Desea cerrar la aplicación del restaurante?",
                parent=self.root
            )
            if not confirmar:
                return
        self.root.destroy()


def main() -> None:
    """Función principal para ejecutar la aplicación gráfica."""
    root = tk.Tk()
    app = AplicacionRestaurante(root)
    root.mainloop()


if __name__ == "__main__":
    main()
