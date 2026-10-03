# -*- coding: utf-8 -*-
import os
import sys
from typing import Callable, Dict, Tuple

# Habilitar soporte de colores ANSI en Windows
if os.name == 'nt':
    os.system('')

# Agregamos la ruta de la aplicación al path de ejecución para resolver las importaciones
directorio_actual = os.path.dirname(os.path.abspath(__file__))
if directorio_actual not in sys.path:
    sys.path.append(directorio_actual)

from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.restaurante import Restaurante

# --- TUPLA (tuple) ---
# Estructura de datos inmutable para definir las opciones del menú principal.
# Garantiza que el menú permanezca estable e inalterable durante toda la ejecución.
MENU_OPCIONES: Tuple[str, ...] = (
    "1. Registrar producto",
    "2. Buscar producto",
    "3. Actualizar producto",
    "4. Eliminar producto",
    "5. Listar productos",
    "6. Registrar usuario",
    "7. Listar usuarios",
    "8. Mostrar categorías",
    "9. Salir"
)

# --- Helpers de Interfaz de Consola ---

def limpiar_pantalla() -> None:
    """Limpia la consola según el sistema operativo."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def pausar(mensaje: str = "Presione Enter para continuar...") -> None:
    """Pausa la ejecución y espera a que el usuario presione Enter."""
    print(f"\n\033[90m--> {mensaje}\033[0m", end="")
    input()


def mostrar_encabezado(titulo: str) -> None:
    """Imprime un encabezado vistoso en consola."""
    limpiar_pantalla()
    ancho = 55
    print("\033[95m" + "=" * ancho)
    print(titulo.center(ancho))
    print("=" * ancho + "\033[0m")


# --- Funciones Manejadoras (UI) ---

def registrar_producto_ui(restaurante: Restaurante) -> None:
    """Captura datos para registrar un Producto y lo envía al servicio."""
    mostrar_encabezado("REGISTRO DE NUEVO PRODUCTO")
    
    while True:
        try:
            print("\033[94mComplete los datos del producto (escriba 'salir' para cancelar):\033[0m\n")
            
            codigo = input("-> Ingrese el código único del producto: ").strip()
            if codigo.lower() == 'salir':
                print("\n\033[93m[!] Registro cancelado por el usuario.\033[0m")
                pausar()
                break
                
            nombre = input("-> Ingrese el nombre del producto: ").strip()
            categoria = input("-> Ingrese la categoría del producto: ").strip()
            precio_raw = input("-> Ingrese el precio del producto: ").strip()
            
            # Validación inicial de formato decimal
            try:
                precio = float(precio_raw)
            except ValueError:
                raise ValueError("El precio debe ser un valor numérico válido.")

            # Instanciamos el producto (los setters validan de forma interna)
            nuevo_producto = Producto(
                codigo=codigo,
                nombre=nombre,
                categoria=categoria,
                precio=precio
            )
            
            # El servicio valida duplicación de código
            restaurante.registrar_producto(nuevo_producto)
            print(f"\n\033[92m[ÉXITO] Producto '{nombre}' registrado con éxito.\033[0m")
            pausar()
            break

        except ValueError as error:
            print(f"\n\033[91m[ERROR] {error}\033[0m")
            reintentar = input("\n¿Desea intentar de nuevo? (S/N): ").strip().upper()
            if reintentar != 'S':
                print("\n\033[93m[!] Registro cancelado.\033[0m")
                pausar()
                break
            mostrar_encabezado("REGISTRO DE NUEVO PRODUCTO")


def buscar_producto_ui(restaurante: Restaurante) -> None:
    """Solicita un código de producto y muestra su información si se encuentra."""
    mostrar_encabezado("BÚSQUEDA DE PRODUCTO")
    codigo = input("-> Ingrese el código del producto a buscar: ").strip()
    
    if not codigo:
        print("\n\033[91m[ERROR] El código de búsqueda no puede estar vacío.\033[0m")
        pausar()
        return

    producto = restaurante.buscar_producto(codigo)
    if producto:
        print("\n\033[92m[ÉXITO] Producto encontrado:\033[0m")
        print("\033[96m" + "-" * 40)
        producto.mostrar_informacion()
        print("-" * 40 + "\033[0m")
    else:
        print(f"\n\033[93m[!] No se encontró ningún producto con el código '{codigo}'.\033[0m")
    pausar()


def actualizar_producto_ui(restaurante: Restaurante) -> None:
    """Permite modificar los datos de un producto existente."""
    mostrar_encabezado("ACTUALIZACIÓN DE PRODUCTO")
    codigo = input("-> Ingrese el código del producto a actualizar: ").strip()
    
    if not codigo:
        print("\n\033[91m[ERROR] El código no puede estar vacío.\033[0m")
        pausar()
        return

    producto = restaurante.buscar_producto(codigo)
    if not producto:
        print(f"\n\033[93m[!] No se encontró ningún producto con el código '{codigo}'.\033[0m")
        pausar()
        return

    print("\n\033[94mProducto seleccionado:\033[0m")
    print(f"Nombre actual: {producto.nombre} | Categoría actual: {producto.categoria} | Precio actual: ${producto.precio:.2f}")
    print("\nIngrese los nuevos datos (presione [Enter] para mantener el valor actual):\n")

    while True:
        try:
            nuevo_nombre_raw = input(f"-> Nuevo nombre [{producto.nombre}]: ").strip()
            nuevo_nombre = nuevo_nombre_raw if nuevo_nombre_raw else producto.nombre

            nueva_categoria_raw = input(f"-> Nueva categoría [{producto.categoria}]: ").strip()
            nueva_categoria = nueva_categoria_raw if nueva_categoria_raw else producto.categoria

            nuevo_precio_raw = input(f"-> Nuevo precio [{producto.precio:.2f}]: ").strip()
            if nuevo_precio_raw:
                try:
                    nuevo_precio = float(nuevo_precio_raw)
                except ValueError:
                    raise ValueError("El precio debe ser un número decimal válido.")
            else:
                nuevo_precio = producto.precio

            # Ejecutamos la actualización mediante el servicio
            restaurante.actualizar_producto(codigo, nuevo_nombre, nueva_categoria, nuevo_precio)
            print(f"\n\033[92m[ÉXITO] Producto '{codigo}' actualizado con éxito.\033[0m")
            pausar()
            break

        except ValueError as error:
            print(f"\n\033[91m[ERROR] {error}\033[0m")
            reintentar = input("\n¿Desea reintentar la edición? (S/N): ").strip().upper()
            if reintentar != 'S':
                print("\n\033[93m[!] Edición cancelada.\033[0m")
                pausar()
                break


def eliminar_producto_ui(restaurante: Restaurante) -> None:
    """Solicita código para eliminar un producto del menú."""
    mostrar_encabezado("ELIMINACIÓN DE PRODUCTO")
    codigo = input("-> Ingrese el código del producto a eliminar: ").strip()
    
    if not codigo:
        print("\n\033[91m[ERROR] El código no puede estar vacío.\033[0m")
        pausar()
        return

    producto = restaurante.buscar_producto(codigo)
    if not producto:
        print(f"\n\033[93m[!] No se encontró ningún producto con el código '{codigo}'.\033[0m")
        pausar()
        return

    print("\n\033[91m[!] ADVERTENCIA: Esta acción no se puede deshacer.\033[0m")
    confirmacion = input(f"¿Está seguro de eliminar el producto '{producto.nombre}'? (S/N): ").strip().upper()
    
    if confirmacion == 'S':
        eliminado = restaurante.eliminar_producto(codigo)
        if eliminado:
            print(f"\n\033[92m[ÉXITO] El producto '{producto.nombre}' ha sido eliminado.\033[0m")
        else:
            print("\n\033[91m[ERROR] No se pudo completar la eliminación.\033[0m")
    else:
        print("\n\033[93m[!] Operación cancelada por el usuario.\033[0m")
    pausar()


def listar_productos_ui(restaurante: Restaurante) -> None:
    """Llama al servicio para listar productos y pausa."""
    limpiar_pantalla()
    restaurante.listar_productos()
    pausar()


def registrar_usuario_ui(restaurante: Restaurante) -> None:
    """Captura datos para registrar un nuevo Usuario."""
    mostrar_encabezado("REGISTRO DE NUEVO USUARIO")
    
    while True:
        try:
            print("\033[94mComplete los datos del usuario (escriba 'salir' para cancelar):\033[0m\n")
            
            identificacion = input("-> Ingrese la identificación / ID del usuario: ").strip()
            if identificacion.lower() == 'salir':
                print("\n\033[93m[!] Registro cancelado por el usuario.\033[0m")
                pausar()
                break
                
            nombre = input("-> Ingrese el nombre del usuario: ").strip()
            correo = input("-> Ingrese el correo electrónico del usuario: ").strip()

            # Instanciamos el usuario (las validaciones corren en los setters)
            nuevo_usuario = Usuario(
                identificacion=identificacion,
                nombre=nombre,
                correo=correo
            )
            
            # El servicio valida duplicación de ID
            restaurante.registrar_usuario(nuevo_usuario)
            print(f"\n\033[92m[ÉXITO] Usuario '{nombre}' registrado con éxito.\033[0m")
            pausar()
            break

        except ValueError as error:
            print(f"\n\033[91m[ERROR] {error}\033[0m")
            reintentar = input("\n¿Desea intentar de nuevo? (S/N): ").strip().upper()
            if reintentar != 'S':
                print("\n\033[93m[!] Registro cancelado.\033[0m")
                pausar()
                break
            mostrar_encabezado("REGISTRO DE NUEVO USUARIO")


def listar_usuarios_ui(restaurante: Restaurante) -> None:
    """Llama al servicio para listar los usuarios registrados y pausa."""
    limpiar_pantalla()
    restaurante.listar_usuarios()
    pausar()


def mostrar_categorias_ui(restaurante: Restaurante) -> None:
    """
    Usa el conjunto (set) obtenido desde el servicio Restaurante
    para listar las categorías únicas de productos cargadas en el sistema.
    """
    mostrar_encabezado("CATEGORÍAS ÚNICAS REGISTRADAS")
    
    # --- CONJUNTO (set) ---
    # Se obtienen las categorías únicas garantizadas por la propiedad matemática de los conjuntos.
    categorias_unicas = restaurante.obtener_categorias_unicas()
    
    if not categorias_unicas:
        print("\n\033[93m[!] No hay productos registrados y, por ende, no existen categorías.\033[0m")
    else:
        print("\n\033[96mCategorías encontradas en el sistema:\033[0m")
        print("\033[90m" + "-" * 40 + "\033[0m")
        for cat in sorted(categorias_unicas):
            print(f"  • {cat}")
        print("\033[90m" + "-" * 40 + "\033[0m")
        print(f"\033[92mTotal de categorías únicas: {len(categorias_unicas)}\033[0m")
        
    pausar()


# --- Función Principal y Ruteo por Diccionario ---

def main() -> None:
    """Punto de entrada de la aplicación y ciclo principal del menú."""
    mi_restaurante = Restaurante("Restaurante El Rincón Gourmet")

    # Precarga de datos iniciales mínimos para evitar que el programa inicie vacío
    # y poder demostrar el funcionamiento de las operaciones de manera inmediata.
    try:
        # Productos de ejemplo
        mi_restaurante.registrar_producto(Producto("P100", "Bife de Chorizo", "Carnes", 18.90))
        mi_restaurante.registrar_producto(Producto("P200", "Limonada Imperial", "Bebidas", 3.50))
        mi_restaurante.registrar_producto(Producto("P300", "Tarta de Tres Leches", "Postres", 4.50))
        mi_restaurante.registrar_producto(Producto("P400", "Costillas BBQ", "Carnes", 22.00))
        
        # Usuarios de ejemplo
        mi_restaurante.registrar_usuario(Usuario("1700000001", "Lilibeth Demera", "lilibeth.d@gourmet.com"))
        mi_restaurante.registrar_usuario(Usuario("1700000002", "Juan Pérez", "juan.perez@gourmet.com"))
    except Exception as e:
        # Silenciamos cualquier error de precarga para asegurar la ejecución limpia
        pass

    # --- DICCIONARIO (dict) ---
    # Estructura clave -> valor que asocia el número de la opción elegida por el usuario
    # con la función correspondiente encargada de resolver la interacción en consola.
    # Reemplaza de forma limpia y profesional una larga cadena de condicionales (if/elif).
    acciones_menu: Dict[str, Callable[[Restaurante], None]] = {
        "1": registrar_producto_ui,
        "2": buscar_producto_ui,
        "3": actualizar_producto_ui,
        "4": eliminar_producto_ui,
        "5": listar_productos_ui,
        "6": registrar_usuario_ui,
        "7": listar_usuarios_ui,
        "8": mostrar_categorias_ui
    }

    while True:
        limpiar_pantalla()
        
        # Imprimir menú iterando sobre la TUPLA
        print("\033[96m========================================")
        print("        SISTEMA DE RESTAURANTE")
        print("========================================")
        for opcion_str in MENU_OPCIONES:
            # Coloreamos visualmente las secciones
            if "Registrar producto" in opcion_str or "Registrar usuario" in opcion_str:
                print(f"\033[92m{opcion_str}\033[0m")
            elif "Salir" in opcion_str:
                print(f"\033[91m{opcion_str}\033[0m")
            else:
                print(f"\033[97m{opcion_str}\033[0m")
        print("\033[96m========================================\033[0m")

        seleccion = input("\033[94mSeleccione una opción (1-9): \033[0m").strip()

        if seleccion == "9":
            mostrar_encabezado("SALIDA DEL SISTEMA")
            print("\n\033[92m¡Gracias por utilizar el Sistema de Restaurante! Hasta pronto.\033[0m\n")
            break
        elif seleccion in acciones_menu:
            # Ruteo directo y dinámico mediante el DICCIONARIO
            acciones_menu[seleccion](mi_restaurante)
        else:
            print("\n\033[91m[!] Opción inválida. Ingrese un valor válido entre 1 y 9.\033[0m")
            pausar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[93m[!] Ejecución interrumpida por el usuario. Saliendo...\033[0m")
        sys.exit(0)
