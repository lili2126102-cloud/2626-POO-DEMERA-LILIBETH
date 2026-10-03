# -*- coding: utf-8 -*-
import os
import sys

# Habilitar soporte de colores ANSI en Windows
if os.name == 'nt':
    os.system('')

# Agregamos la ruta de la aplicación al path de ejecución para resolver las importaciones
directorio_actual = os.path.dirname(os.path.abspath(__file__))
if directorio_actual not in sys.path:
    sys.path.append(directorio_actual)

from modelos.producto import Producto
from modelos.bebida import Bebida
from modelos.cliente import Cliente
from servicios.restaurante import Restaurante


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
    ancho = 50
    print("\033[95m" + "=" * ancho)
    print(titulo.center(ancho))
    print("=" * ancho + "\033[0m")


def registrar_producto_ui(restaurante: Restaurante) -> None:
    """Captura datos para registrar un Producto y lo envía al servicio."""
    mostrar_encabezado("REGISTRO DE NUEVO PRODUCTO")
    
    while True:
        try:
            print("\033[94mComplete los datos del producto (escriba 'salir' para cancelar):\033[0m\n")
            
            codigo = input("-> Ingrese el código único del producto: ").strip()
            if codigo.lower() == 'salir':
                print("\n\033[93m[!] Registro cancelado por el usuario.\033[0m")
                break
                
            nombre = input("-> Ingrese el nombre del producto: ").strip()
            categoria = input("-> Ingrese la categoría del producto: ").strip()
            precio_raw = input("-> Ingrese el precio del producto: ").strip()
            
            # Validación inicial del precio antes de instanciar
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


def registrar_bebida_ui(restaurante: Restaurante) -> None:
    """Captura datos para registrar una Bebida (hija de Producto) y la envía al servicio."""
    mostrar_encabezado("REGISTRO DE NUEVA BEBIDA")
    
    while True:
        try:
            print("\033[94mComplete los datos de la bebida (escriba 'salir' para cancelar):\033[0m\n")
            
            codigo = input("-> Ingrese el código único de la bebida: ").strip()
            if codigo.lower() == 'salir':
                print("\n\033[93m[!] Registro cancelado por el usuario.\033[0m")
                break
                
            nombre = input("-> Ingrese el nombre de la bebida: ").strip()
            categoria = input("-> Ingrese la categoría de la bebida (ej. Refresco, Caliente): ").strip()
            precio_raw = input("-> Ingrese el precio de la bebida: ").strip()
            tamano = input("-> Ingrese el tamaño de la bebida (ej. 500ml, Familiar): ").strip()
            tipo_envase = input("-> Ingrese el tipo de envase (ej. Vidrio, Lata, Plástico): ").strip()
            
            # Validación inicial de precio
            try:
                precio = float(precio_raw)
            except ValueError:
                raise ValueError("El precio debe ser un valor numérico válido.")

            # Instanciamos la bebida (los setters validan de forma interna)
            nueva_bebida = Bebida(
                codigo=codigo,
                nombre=nombre,
                categoria=categoria,
                precio=precio,
                tamano=tamano,
                tipo_envase=tipo_envase
            )
            
            # El servicio valida duplicación de código
            restaurante.registrar_producto(nueva_bebida)
            print(f"\n\033[92m[ÉXITO] Bebida '{nombre}' registrada con éxito.\033[0m")
            pausar()
            break

        except ValueError as error:
            print(f"\n\033[91m[ERROR] {error}\033[0m")
            reintentar = input("\n¿Desea intentar de nuevo? (S/N): ").strip().upper()
            if reintentar != 'S':
                print("\n\033[93m[!] Registro cancelado.\033[0m")
                pausar()
                break
            mostrar_encabezado("REGISTRO DE NUEVA BEBIDA")


def registrar_cliente_ui(restaurante: Restaurante) -> None:
    """Captura datos para registrar un Cliente y lo envía al servicio."""
    mostrar_encabezado("REGISTRO DE NUEVO CLIENTE")
    
    while True:
        try:
            print("\033[94mComplete los datos del cliente (escriba 'salir' para cancelar):\033[0m\n")
            
            identificacion = input("-> Ingrese la identificación / ID del cliente: ").strip()
            if identificacion.lower() == 'salir':
                print("\n\033[93m[!] Registro cancelado por el usuario.\033[0m")
                break
                
            nombre = input("-> Ingrese el nombre del cliente: ").strip()
            correo = input("-> Ingrese el correo electrónico del cliente: ").strip()

            # Instanciamos el cliente (los setters validan de forma interna)
            nuevo_cliente = Cliente(
                identificacion=identificacion,
                nombre=nombre,
                correo=correo
            )
            
            # El servicio valida duplicación de identificación
            restaurante.registrar_cliente(nuevo_cliente)
            print(f"\n\033[92m[ÉXITO] Cliente '{nombre}' registrado con éxito.\033[0m")
            pausar()
            break

        except ValueError as error:
            print(f"\n\033[91m[ERROR] {error}\033[0m")
            reintentar = input("\n¿Desea intentar de nuevo? (S/N): ").strip().upper()
            if reintentar != 'S':
                print("\n\033[93m[!] Registro cancelado.\033[0m")
                pausar()
                break
            mostrar_encabezado("REGISTRO DE NUEVO CLIENTE")


def listar_productos_ui(restaurante: Restaurante) -> None:
    """Muestra la lista polimórfica de productos en el servicio."""
    limpiar_pantalla()
    restaurante.listar_productos()
    pausar()


def listar_clientes_ui(restaurante: Restaurante) -> None:
    """Muestra la lista de clientes en el servicio."""
    limpiar_pantalla()
    restaurante.listar_clientes()
    pausar()


def main() -> None:
    """Función de arranque principal y control del menú del sistema."""
    mi_restaurante = Restaurante("El Rincón del Sabor")

    # Registro inicial de prueba (opcional, pero ayuda a evidenciar el funcionamiento)
    # según el requisito "Evitar objetos principales definidos únicamente con valores quemados"
    # permitiremos que empiece vacío o que el usuario registre interactivamente todo.
    # Para cumplir mejor con la interacción dinámica, mantendremos la lista inicial limpia o con datos de prueba
    # que faciliten ver el polimorfismo inmediatamente. Agregaremos 2 productos de prueba por defecto.
    try:
        mi_restaurante.registrar_producto(Producto("P001", "Lasaña de Carne", "Almuerzo", 8.50))
        mi_restaurante.registrar_producto(Bebida("B001", "Jugo de Mora Natural", "Bebida Fria", 2.00, "400ml", "Vidrio"))
        mi_restaurante.registrar_cliente(Cliente("1712345678", "Lilibeth Demera", "lilibeth.demera@correo.com"))
    except Exception:
        pass # Prevenir cualquier error al cargar los datos iniciales

    while True:
        limpiar_pantalla()
        
        # Despliegue del menú interactivo obligatorio
        print("\033[96m========================================")
        print("        SISTEMA DE RESTAURANTE")
        print("========================================")
        print("1. Registrar producto")
        print("2. Registrar bebida")
        print("3. Registrar cliente")
        print("----------------------------------------")
        print("4. Listar productos")
        print("5. Listar clientes")
        print("----------------------------------------")
        print("6. Salir")
        print("========================================\033[0m")

        opcion = input("\033[94mSeleccione una opción (1-6): \033[0m").strip()

        if opcion == "1":
            registrar_producto_ui(mi_restaurante)
        elif opcion == "2":
            registrar_bebida_ui(mi_restaurante)
        elif opcion == "3":
            registrar_cliente_ui(mi_restaurante)
        elif opcion == "4":
            listar_productos_ui(mi_restaurante)
        elif opcion == "5":
            listar_clientes_ui(mi_restaurante)
        elif opcion == "6":
            mostrar_encabezado("SALIDA DEL SISTEMA")
            print("\n\033[92m¡Gracias por utilizar el Sistema de Restaurante! Hasta pronto.\033[0m\n")
            break
        else:
            print("\n\033[91m[!] Opción inválida. Seleccione un número entre 1 y 6.\033[0m")
            pausar()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n\033[93m[!] Ejecución interrumpida por el usuario. Saliendo...\033[0m")
        sys.exit(0)
